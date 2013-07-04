#coding=utf-8
#python3
import urllib
from http.cookiejar import CookieJar
import time
import traceback
import gzip


class HttpUtil():
    def __init__(self,proxy = None, headers = None):
        #proxy = {'http': 'http://210.14.143.53:7620'}
        if proxy != None:
            pass
            proxy_handler = urllib.request.ProxyHandler(proxy)
            self.opener = urllib.request.build_opener(proxy_handler,urllib.request.HTTPCookieProcessor(CookieJar()))
        else:
            pass
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
        if not headers:
            self.opener.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'),\
                                ]


    def Get(self,url,times=1):
        for i in range(times):
            try:
                resp = self.opener.open(url)
                return resp.read()
            except:
                time.sleep(1)
                print(traceback.format_exc())
                continue
        
        return None
    
    def Post(self,url,data,times=1):
        for i in range(times):
            try:
                resp = self.opener.open(url,data)
                return resp.read()
            except:
                time.sleep(1)
                print(traceback.format_exc())
                continue
        return None
    
    def real_url(self,url,times=1):
        for i in range(times):
            try:
                return self.opener.open(url).geturl()
            except:
                time.sleep(1)
                print(traceback.format_exc())
                continue
        return None
    
    def unzip(self,data):
        import gzip
        from io import StringIO
        data = StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data

        
if __name__ =='__main__':
    httpUtil = HttpUtil()
    content = httpUtil.Get('http://lol.duowan.com/1108/m_178050471525.html')
    print(httpUtil.unzip(content))
    print(len(content))
