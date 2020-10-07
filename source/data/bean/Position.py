#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/7 18:46
# @Author : NJU
# @Version：V 0.1
# @File : Position.py
# @desc :


from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class Position(BeanBase):
    """ gitlab 数据 position 数据 共计9个

    """

    def __init__(self):
        self.notes_id = None
        self.base_sha = None
        self.head_sha = None
        self.start_sha = None
        self.old_path = None
        self.new_path = None
        self.position_type = None
        self.old_line = None
        self.new_line = None

    @staticmethod
    def getIdentifyKeys():
        items = [StringKeyUtils.STR_KEY_NOTES_ID]
        return items

    @staticmethod
    def getItemKeyList():
        items = [StringKeyUtils.STR_KEY_NOTES_ID, StringKeyUtils.STR_KEY_BASE_SHA,
                 StringKeyUtils.STR_KEY_HEAD_SHA, StringKeyUtils.STR_KEY_START_SHA,
                 StringKeyUtils.STR_KEY_OLD_PATH, StringKeyUtils.STR_KEY_NEW_PATH,
                 StringKeyUtils.STR_KEY_POSITION_TYPE, StringKeyUtils.STR_KEY_OLD_LINE,
                 StringKeyUtils.STR_KEY_NEW_LINE]

        return items

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_PROJECT_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_IID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_BASE_SHA, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_HEAD_SHA, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_START_SHA, BeanBase.DATA_TYPE_STRING)]

        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_NOTES_ID: self.notes_id,
                 StringKeyUtils.STR_KEY_BASE_SHA: self.base_sha,
                 StringKeyUtils.STR_KEY_HEAD_SHA: self.head_sha,
                 StringKeyUtils.STR_KEY_START_SHA: self.start_sha,
                 StringKeyUtils.STR_KEY_OLD_PATH: self.old_path,
                 StringKeyUtils.STR_KEY_NEW_PATH: self.new_path,
                 StringKeyUtils.STR_KEY_POSITION_TYPE: self.position_type,
                 StringKeyUtils.STR_KEY_OLD_LINE: self.old_line,
                 StringKeyUtils.STR_KEY_NEW_LINE: self.new_line}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = Position()
                res.notes_id = src.get(StringKeyUtils.STR_KEY_NOTES_ID)
                res.base_sha = src.get(StringKeyUtils.STR_KEY_BASE_SHA)
                res.head_sha = src.get(StringKeyUtils.STR_KEY_HEAD_SHA)
                res.start_sha = src.get(StringKeyUtils.STR_KEY_START_SHA)
                res.old_path = src.get(StringKeyUtils.STR_KEY_OLD_PATH)
                res.new_path = src.get(StringKeyUtils.STR_KEY_NEW_PATH)
                res.position_type = src.get(StringKeyUtils.STR_KEY_POSITION_TYPE)
                res.old_line = src.get(StringKeyUtils.STR_KEY_OLD_LINE)
                res.new_line = src.get(StringKeyUtils.STR_KEY_NEW_LINE)

            return res
