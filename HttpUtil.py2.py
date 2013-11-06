#coding=utf-8
import urllib2
import cookielib
import HTMLParser
import time
import traceback
import gzip
import json


class HttpUtil():
    def __init__(self,headers = None,proxy = None):
        #proxy = {'http': 'http://210.14.143.53:7620'}
        if proxy != None:
            proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(proxy_handler,urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        else:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

        if headers:
            self.opener.addheaders = headers
        else:
            self.opener.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'),\
                                ]

    def Get(self,url,times=1,timeout=30):
        for i in range(times):
            try:
                resp = self.opener.open(url,timeout=timeout)
                return resp.read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue

        return None

    def Post(self,url,data,times=1, timeout=30):
        for i in range(times):
            try:
                resp = self.opener.open(url,data,timeout=timeout)
                return resp.read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        return None

    def real_url(self,url,times=1,timeout=30):
        for i in range(times):
            try:
                return self.opener.open(url,timeout=timeout).geturl()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        return None

    def unzip(self,data):
        import gzip
        import StringIO
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data


if __name__ =='__main__':
    httpUtil = HttpUtil()
    content = httpUtil.Get('http://lol.duowan.com/1108/m_178050471525.html')
    print httpUtil.unzip(content)
    print len(content)
