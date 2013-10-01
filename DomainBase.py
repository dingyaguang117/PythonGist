#coding=utf-8
'''
1.定义方法见Resource类
注意：成员字段不能以双下划线"__"开始
PS：后面带默认值，且赋值的时候不做类型检查

2.getInsertDict 方法，获得所有字段的字典，未赋值字段为默认

3.getUpdateDict 方法，获得赋值字段的字典

'''

class DomainBase():
    def __init__(self):
        self.data = {}
        
    def __setitem__(self,key,value):
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found'%key)
        self.data[key] = value
    
    def __getitem__(self,key):
        if key in self.data:
            return self.data[key]
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found'%key)
        return self.__class__.__dict__[key]
    
    
    def getInsertDict(self):
        ret = {}
        for key in self.__class__.__dict__:
            if key.startswith('__'):continue
            if key not in self.data:
                ret[key] = self.__class__.__dict__[key]
            else:
                ret[key] = self.data[key]
        return ret
    
    def getUpdateDict(self):
        return self.data





class Resource(DomainBase):
    resourceSize = -1
    resourceUrl = ''
    resourceName = ''
    resourceImageUrl = ''
    duration = -1
    channelId = -1
    categoryId = -1