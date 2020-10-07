#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/7 19:59
# @Author : NJU
# @Version：V 0.1
# @File : Diff.py
# @desc :
from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class Diff(BeanBase):
    """ gitlab 数据  diff数据
        注： commit 比较产生的中途数据，不存入数据库
    """

    def __init__(self):
        self.old_path = None
        self.new_path = None
        self.new_file = None
        self.renamed_file = None
        self.deleted_file = None
        self.diff = None

    @staticmethod
    def getIdentifyKeys():
        raise Exception("can not store in database!")
        items = [StringKeyUtils.STR_KEY_OLD_PATH, StringKeyUtils.STR_KEY_NEW_PATH]
        return items

    @staticmethod
    def getItemKeyList():
        raise Exception("can not store in database!")
        items = [StringKeyUtils.STR_KEY_OLD_PATH, StringKeyUtils.STR_KEY_NEW_PATH,
                 StringKeyUtils.STR_KEY_NEW_FILE, StringKeyUtils.STR_KEY_RENAMED_FILE,
                 StringKeyUtils.STR_KEY_DELETED_FILE, StringKeyUtils.STR_KEY_DIFF]

        return items

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_OLD_PATH, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_NEW_PATH, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_NEW_FILE, BeanBase.DATA_TYPE_BOOLEAN),
                 (StringKeyUtils.STR_KEY_RENAMED_FILE, BeanBase.DATA_TYPE_BOOLEAN),
                 (StringKeyUtils.STR_KEY_DELETED_FILE, BeanBase.DATA_TYPE_BOOLEAN),
                 (StringKeyUtils.STR_KEY_DIFF, BeanBase.DATA_TYPE_STRING)]

        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_OLD_PATH: self.old_path,
                 StringKeyUtils.STR_KEY_NEW_PATH: self.new_path,
                 StringKeyUtils.STR_KEY_NEW_FILE: self.new_file,
                 StringKeyUtils.STR_KEY_RENAMED_FILE: self.renamed_file,
                 StringKeyUtils.STR_KEY_DELETED_FILE: self.deleted_file,
                 StringKeyUtils.STR_KEY_DIFF: self.diff}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = Diff()
                res.old_path = src.get(StringKeyUtils.STR_KEY_OLD_PATH, None)
                res.new_path = src.get(StringKeyUtils.STR_KEY_NEW_PATH, None)
                res.new_file = src.get(StringKeyUtils.STR_KEY_NEW_FILE, None)
                res.renamed_file = src.get(StringKeyUtils.STR_KEY_RENAMED_FILE, None)
                res.deleted_file = src.get(StringKeyUtils.STR_KEY_DELETED_FILE, None)
                res.diff = src.get(StringKeyUtils.STR_KEY_DIFF, None)

            return res
