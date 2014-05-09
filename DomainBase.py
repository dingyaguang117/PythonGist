#coding=utf-8
'''
1.定义方法见Resource类
注意：成员字段不能以双下划线"__"开始
PS：后面带默认值，且赋值的时候不做类型检查

2.getInsertDict 方法，获得所有字段的字典，未赋值字段为默认

3.getUpdateDict 方法，获得赋值字段的字典

'''

class DomainBase(object):
    def __init__(self):
        #注意这里，如果用 self.data = {} 会触发__setattr__导致非预期效果
        #这里把成员存储在名为data的字典里面而不是直接存在 __dict__的原因是，会导致循环递归爆栈
        #self.__dict__['data'] = {}
        pass

    def __setitem__(self, key, value):
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found' % key)
        self.__dict__[key] = value

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found' % key)
        return self.__class__.__dict__[key]

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def getInsertDict(self):
        ret = {}
        for key in self.__class__.__dict__:
            if key.startswith('__'):continue
            if key not in self.__dict__:
                ret[key] = self.__class__.__dict__[key]
            else:
                ret[key] = self.__dict__[key]
        return ret

    def getUpdateDict(self):
        return self.__dict__

    def update(self, data, **kwargs):
        for key in kwargs:
            data[key] = kwargs[key]
        self.__dict__.update(data)
        return self

    def pop(self, key):
        return self.__dict__.pop(key)


class Contact(DomainBase):
    uid = 'default'
    first_name = ''
    last_name = ''
    nick_name = ''
    home_phone = ''
    email = ''
    company = ''
    department = ''
    birthday = ''
    blog_index = ''
    createTime = ''


if __name__ == '__main__':
    pass
    #print GiveAway().getInsertDict()
    c = Contact()
    # print 'dir(c) : ', dir(c)
    # print 'c.__dict__ : ', c.__dict__
    # print type(c)
    c.uid = '1'
    c.first_name = 33
    print 'c.email', c.email
    print 'c.uid:', c.uid
    print c.getInsertDict()
    print c.getUpdateDict()

    c['uid'] = 3
    c['company'] = '22'
    print c.getInsertDict()
    print c.getUpdateDict()
