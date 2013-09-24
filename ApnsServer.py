'''
使用redis实现的苹果push服务
支持多线程，安全退出
'''
from APNSWrapper import APNSNotificationWrapper
from APNSWrapper import APNSNotification
import redis
import Queue
from threading import Thread
import threading
import time,sys,signal,logging
from PushHandle import handle


class ApnsServer():
    UNSTART = 'unstart'
    RUNNING = 'running'
    GET_STOP = 'getStop'
    WORK_STOP = 'workStop'
    STOPED  = 'stoped'
    
    
    def __init__(self,host,handle,pem,threadNum = 10,sendLength=10,loglevel=logging.WARNING):
        self.threadNum = threadNum
        self.handle = handle
        self.host = host #('60.28.29.49',6379,0,'test')
        self.redis = redis.Redis(host=host[0], port=host[1],db=host[2])
        self.keyname = host[3]
        self.tashQueue = Queue.Queue()
        self.sendLength = sendLength
        self.status = self.UNSTART
        self.pemfilename = pem[0]
        self.sandbox = pem[1]
        self.taskThreads = []
        self.loglevel = loglevel
        self.logger = logging.getLogger()
        self.logger.setLevel(loglevel)
        handle = logging.StreamHandler(sys.stdout)
        handle.setFormatter(logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s'))
        self.logger.addHandler(handle)
        
        
    def getTask(self):
        self.logger.warning('GetTask Thread started')
        while self.status != self.GET_STOP:
            if self.tashQueue.qsize() > self.threadNum * self.sendLength * 5:
                self.logger.info('taskQueue full,sleep 1s')
                time.sleep(1)
                continue
            taskstr = self.redis.blpop(self.keyname,timeout=3)
            if taskstr == None:
                self.logger.warning('redis pop null')
                continue
            else:
                self.tashQueue.put(taskstr[1])
        self.logger.warning('GetTask Thread exited')
    
    
    def taskThreadProc(self):
        self.logger.warning('%s started'%threading.currentThread().getName())
        apnsWrapper = APNSNotificationWrapper(self.pemfilename, self.sandbox)
        while self.status != self.WORK_STOP:
            self.logger.debug('%s : apnsWrapper.count()=%d'%(threading.currentThread().getName(),apnsWrapper.count()))
            if apnsWrapper.count() == 0:
                try:
                    taskstr = self.tashQueue.get(timeout=10)
                except Queue.Empty,e:
                    self.logger.info('%s Get 0 task in 10s'%(threading.currentThread().getName()))
                    continue
            else:
                try:
                    taskstr = self.tashQueue.get(timeout=1)
                except Queue.Empty,e:
                    self.logger.info('%s is to notify %d push'%(threading.currentThread().getName(),apnsWrapper.count()))
                    result = apnsWrapper.notify()
                    self.logger.info('%s notified %d push:%s'%(threading.currentThread().getName(),apnsWrapper.count(),result))
                    apnsWrapper = APNSNotificationWrapper(self.pemfilename, self.sandbox)
                    continue
            self.logger.debug('%s Get taskstr:%s'%(threading.currentThread().getName(),taskstr))
            try:
                message = None
                message = self.handle(taskstr)
            except:
                self.logger.error('handle error taskstr:\n%s'%(taskstr))
                import traceback
                print traceback.format_exc()
                
            if message == None:
                self.logger.warning('drop task %s'%taskstr)
                continue
            else:
                self.logger.debug('parse task success:\n'+message._build())
            apnsWrapper.append(message)
            if apnsWrapper.count() == self.sendLength:
                self.logger.info('%s is to notify %d push'%(threading.currentThread().getName(),apnsWrapper.count()))
                result = apnsWrapper.notify()
                self.logger.info('%s notified %d push:%s'%(threading.currentThread().getName(),apnsWrapper.count(),result))
                apnsWrapper = APNSNotificationWrapper(self.pemfilename, self.sandbox)
        if apnsWrapper.count() > 0:
            result = apnsWrapper.notify()
        self.logger.warning('%s exited'%threading.currentThread().getName())
        
    def serve_forever(self):
        for i in xrange(self.threadNum):
            thread = Thread(target=self.taskThreadProc)#,args=(self,))
            thread.start()
            self.taskThreads.append(thread)
        self.status = self.RUNNING
        self.getTask()
        while self.tashQueue.qsize() >0:
            self.logger.warning('wait taskQueue empty...(now %d)'%self.tashQueue.qsize())
            aliveThreadNum = reduce(lambda num,one:num+1 if one.isAlive() else num,self.taskThreads,0)
            self.logger.warning('alive thread num =%d'%aliveThreadNum)
            if aliveThreadNum == 0:
                self.logger.warning('no alive thread,write task back..')
                while self.tashQueue.qsize() != 0:
                    s = self.tashQueue.get(timeout=1)
                    self.redis.lpush(self.keyname,s)
                        
            time.sleep(1)
        self.status = self.WORK_STOP
        self.logger.warning('wait all thread exit...')
        for t in self.taskThreads:
            t.join()
        self.logger.warning('exited')
        
    
    
    def stop(self,sig,stack):
        self.logger.warning('prepare to exit...')
        self.status = self.GET_STOP
        
        
def main():
    #server = ApnsServer(('60.28.29.49',6379,0,'anteaterPush'),handle,('../pem/ck.pem',True),sendLength=1,loglevel=logging.DEBUG)
    server = ApnsServer(('60.28.29.49',6379,0,'anteaterPush'),handle,('../pem/ck_production.pem',False),sendLength=1,loglevel=logging.DEBUG)
    signal.signal(signal.SIGINT,server.stop)
    server.serve_forever()
    
    
if __name__ == '__main__':
    main()
