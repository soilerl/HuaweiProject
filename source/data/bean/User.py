# coding=gbk
from datetime import datetime

from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class User(BeanBase):
    """ gitlab用户类数据  共计4个

    """

    def __init__(self):
        self.id = None
        self.name = None
        self.username = None
        self.state = None

    @staticmethod
    def getIdentifyKeys():
        return [StringKeyUtils.STR_KEY_USER_NAME]

    @staticmethod
    def getItemKeyList():
        items = [StringKeyUtils.STR_KEY_ID, StringKeyUtils.STR_KEY_NAME,
                 StringKeyUtils.STR_KEY_USER_NAME, StringKeyUtils.STR_KEY_STATE]

        return items

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_USER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_STATE, BeanBase.DATA_TYPE_STRING)]

        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_ID: self.id,
                 StringKeyUtils.STR_KEY_NAME: self.name,
                 StringKeyUtils.STR_KEY_USER_NAME: self.username,
                 StringKeyUtils.STR_KEY_STATE: self.state}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = User()
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.name = src.get(StringKeyUtils.STR_KEY_NAME, None)
                res.username = src.get(StringKeyUtils.STR_KEY_USER_NAME, None)
                res.state = src.get(StringKeyUtils.STR_KEY_STATE, None)

            return res

