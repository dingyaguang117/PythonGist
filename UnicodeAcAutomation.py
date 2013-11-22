#coding=utf-8

#KIND = 16
#BASE = ord('a')
import math

class Node():
    static = 0
    def __init__(self,KIND):
        self.fail = None
        self.next = [None]*KIND
        self.end = False
        self.word = None
        Node.static += 1

class AcAutomation():
    def __init__(self,KIND=16):
        self.root = Node(KIND)
        self.queue = []
        self.KIND = KIND
        
    def getIndex(self,char):
        return ord(char)# - BASE
    
    def insert(self,string):
        p = self.root
        for char in string:
            index = self.getIndex(char)
            if p.next[index] == None:
                p.next[index] = Node(self.KIND)
            p = p.next[index]
        p.end = True
        p.word = string
        
    def build_automation(self):
        self.root.fail = None
        self.queue.append(self.root)
        while len(self.queue)!=0:
            parent = self.queue[0]
            self.queue.pop(0)
            for i,child in enumerate(parent.next):
                if child == None:continue
                if parent == self.root:
                    child.fail = self.root
                else:
                    failp = parent.fail
                    while failp != None:
                        if failp.next[i] != None:
                            child.fail = failp.next[i]
                            break
                        failp = failp.fail
                    if failp==None: child.fail=self.root
                self.queue.append(child)
                
    def matchOne(self,string):
        p = self.root
        for char in string:
            index = self.getIndex(char)
            while p.next[index]==None and p!=self.root: p=p.fail
            if p.next[index]==None:p=self.root
            else: p=p.next[index]
            if p.end:return True,p.word
        return False,None
    
    


class UnicodeAcAutomation():
    def __init__(self,KIND=16,encoding='utf-8'):
        '''
            KIND must can be 2^i  at most 2^8
        '''
        self.ac = AcAutomation(KIND)
        self.encoding = encoding
        self.KIND = KIND
        self.KNUM = int(math.log(256)/math.log(KIND) + 0.1)
        print self.KIND,self.KNUM
        
    def getAcString(self,string):
        string = bytearray(string.encode(self.encoding))
        ac_string = ''
        for byte in string:
            for i in xrange(self.KNUM):
                ac_string += chr(byte%self.KIND)
                byte /= self.KIND
        return ac_string
    
    def insert(self,string):
        if type(string) != unicode:
            raise Exception('UnicodeAcAutomation:: insert type not unicode')
        ac_string = self.getAcString(string)
        self.ac.insert(ac_string)

    def build_automation(self):
        self.ac.build_automation()
    
    def matchOne(self,string):
        if type(string) != unicode:
            raise Exception('UnicodeAcAutomation:: insert type not unicode')
        ac_string = self.getAcString(string)
        retcode,ret = self.ac.matchOne(ac_string)
        if ret!=None:
            s = ''
            for i in range(len(ret)/self.KNUM):
                base = 1
                c = 0
                for j in xrange(self.KNUM):
                    c += ord(ret[self.KNUM*i+j]) * base
                    base *= self.KIND
                s += chr(c)
            ret = s.decode(self.encoding)
        return retcode,ret
    


def main2():
    ac = UnicodeAcAutomation()
    ac.insert(u'丁亚光')
    ac.insert(u'好吃的')
    ac.insert(u'好玩的')
    ac.build_automation()
    print ac.matchOne(u'hi,丁亚光在干啥')
    print ac.matchOne(u'ab')
    print ac.matchOne(u'不能吃饭啊')
    print ac.matchOne(u'饭很好吃，有很多好好的吃的，')
    print ac.matchOne(u'有很多好玩的')

if __name__ == '__main__':
    main2()
    
