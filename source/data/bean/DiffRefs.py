#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/7 9:52
# @Author : NJU
# @Version：V 0.1
# @File : DiffRefs.py
# @desc :
from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class DiffRefs(BeanBase):
    """ gitlab 数据  diffrefs 数据 共计3个

    """

    def __init__(self):
        self.base_sha = None
        self.head_sha = None
        self.start_sha = None
        self.project_id = None  # 用于merge request和diff_refs连接手动添加的属性
        self.iid = None

    @staticmethod
    def getIdentifyKeys():
        items = [StringKeyUtils.STR_KEY_PROJECT_ID, StringKeyUtils.STR_KEY_IID,
                 StringKeyUtils.STR_KEY_BASE_SHA, StringKeyUtils.STR_KEY_HEAD_SHA,
                 StringKeyUtils.STR_KEY_START_SHA]
        return items

    @staticmethod
    def getItemKeyList():
        items = [StringKeyUtils.STR_KEY_PROJECT_ID, StringKeyUtils.STR_KEY_IID,
                 StringKeyUtils.STR_KEY_BASE_SHA, StringKeyUtils.STR_KEY_HEAD_SHA,
                 StringKeyUtils.STR_KEY_START_SHA]

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
        items = {StringKeyUtils.STR_KEY_PROJECT_ID: self.project_id,
                 StringKeyUtils.STR_KEY_IID: self.iid,
                 StringKeyUtils.STR_KEY_BASE_SHA: self.base_sha,
                 StringKeyUtils.STR_KEY_HEAD_SHA: self.head_sha,
                 StringKeyUtils.STR_KEY_START_SHA: self.start_sha}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = DiffRefs()
                res.base_sha = src.get(StringKeyUtils.STR_KEY_BASE_SHA, None)
                res.head_sha = src.get(StringKeyUtils.STR_KEY_HEAD_SHA, None)
                res.start_sha = src.get(StringKeyUtils.STR_KEY_START_SHA, None)

            return res

