# _*_ coding: utf-8 _*_

class BeanBase:
    """所有数据类的基类"""

    @staticmethod
    def getItemKeyList():
        pass

    '''提供数据项名名字列表'''

    @staticmethod
    def getItemKeyListWithType():
        pass

    '''提供数据项名字和种类元组列表'''

    def getValueDict(self):
        pass

    '''提供该类所有数据字典'''

    @staticmethod
    def getIdentifyKeys():
        pass

    '''提供数据类的唯一标识'''

    '''数据项中涉及的种类'''
    DATA_TYPE_INT = 0
    DATA_TYPE_DATE_TIME = 1
    DATA_TYPE_STRING = 2
    DATA_TYPE_TEXT = 3
    DATA_TYPE_BOOLEAN = 4
    DATA_TYPE_LONG_TEXT = 5

    class parser:
        '''用于解析json的数据类'''

        @staticmethod
        def parser(src):
            pass

        '''解析json 返回数据类'''
