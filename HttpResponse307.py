'''
Django 没办法返回307 code
(307跳转是防止POST被修改成GET请求)
只有自定义一个
'''

from django.http import HttpResponse

class HttpResponse307(HttpResponse):
    status_code = 307
    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['Location'] = redirect_to
