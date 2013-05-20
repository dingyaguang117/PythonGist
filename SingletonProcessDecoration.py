#coding=utf-8
#@author dingyaguang

import os

def SingletonProcessDecoration(filename):
    def _deco(func):
        def __deco(*args, **kwargs):
            if os.path.exists(filename):
                print 'lockfile %s exists..program exit...'%filename
                return
            open(filename,'w').close()
            ret = func(*args, **kwargs)
            os.remove(filename)
            return ret
        return __deco
    return _deco


@SingletonProcessDecoration('1.lock')
def main():
    import time
    time.sleep(3)
    return True
    
if __name__ == '__main__':
    print main()
