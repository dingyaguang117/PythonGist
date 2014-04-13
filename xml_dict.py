__author__ = 'ding'
#coding=utf-8
#@author dingyaguang
'''
实现xml和python字典之间的互相转换
规则为：
1. node的attribute全部忽略
2. xml转换到dict的时候，root的tag会被忽略掉，所以结果的最外层的key为xml的第一级子节点的tag
3. dict转xml第2条的逆向，所以需要手动指定一个root的tag
4. xml中有相同tag名的兄弟节点，在转换成dict的时候会变成一个list(因为python的dict是hash字典，不允许重复key)
5. xml2dict的参数是一个字符串或者Element对象 返回的结果是一个dict
6. dict2xml的参数是一个dict,返回的是一个Element对象，可以使用xml_tostring 方法转换为字符串
'''

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

def xml2dict(element):
    if type(element) in [str, unicode]:
        element = ET.fromstring(element)
    assert isinstance(element, Element)
    ret = {}
    for child in list(element):
        #print child.tag, child.text
        if len(child) != 0:
            value = xml2dict(child)
        else:
            value = child.text
        if child.tag in ret:
            if type(ret[child.tag]) != list:
                ret[child.tag] = [ret[child.tag]]
            ret[child.tag].append(value)
        else:
            ret[child.tag] = value
    return ret


def dict2xml(root, content):
    if type(content) in [str, unicode, int, long, float]:
        e = Element(root)
        e.text = content
        return e

    e = Element(root)
    for key in content:
        if type(content[key]) == list:
            for one in content[key]:
                e.append(dict2xml(key, one))
        else:
            e.append(dict2xml(key, content[key]))
    return e


xml_tostring = ET.tostring


#=============================================================

def testXml2Json():
    s = '''
    <xml>
     <ToUserName><![CDATA[toUser]]></ToUserName>
     <FromUserName><![CDATA[fromUser]]></FromUserName>
     <CreateTime>1348831860</CreateTime>
     <MsgType><![CDATA[text]]></MsgType>
     <Content><![CDATA[this is a test]]></Content>
     <MsgId>1234567890123456</MsgId>
     </xml>
    '''

    s2 = '''
    <root>
         <person age="18">
            <name>hzj</name>
            <sex>man</sex>
         </person>
         <person age="19" des="hello">
            <name>kiki</name>
            <sex>female</sex>
         </person>
         <person2 age="19" des="hello">
            <name>kiki</name>
            <sex>female</sex>
         </person2>
        </root>
    '''

    print xml2dict(ET.fromstring(s2))

def testJson2xml():
    d = {'a':'4234','b':[{'a':'1'},{'b':'2'}]}
    print dict2xml('xml',d)
    print xml2dict(dict2xml('xml',d))



if __name__ == '__main__':
    testXml2Json()
    #testJson2xml()
