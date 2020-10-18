#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/17 16:23
# @Author : NJU
# @Version：V 0.1
# @File : Pipelines.py
# @desc :
from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class Pipelines(BeanBase):
    """ gitlab 数据  pipelines 数据 共计3个

    """

    def __init__(self):
        self.project_id = None
        self.merge_request_id = None
        self.id = None
        self.iid = None
        self.sha = None

    @staticmethod
    def getIdentifyKeys():
        items = [StringKeyUtils.STR_KEY_PROJECT_ID, StringKeyUtils.STR_KEY_MERGE_REQUEST_ID,
                 StringKeyUtils.STR_KEY_ID, StringKeyUtils.STR_KEY_IID]
        return items

    @staticmethod
    def getItemKeyList():
        items = [StringKeyUtils.STR_KEY_PROJECT_ID, StringKeyUtils.STR_KEY_MERGE_REQUEST_ID,
                 StringKeyUtils.STR_KEY_ID, StringKeyUtils.STR_KEY_IID,
                 StringKeyUtils.STR_KEY_SHA]

        return items

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_PROJECT_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_MERGE_REQUEST_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_IID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_SHA, BeanBase.DATA_TYPE_STRING)]

        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_PROJECT_ID: self.project_id,
                 StringKeyUtils.STR_KEY_MERGE_REQUEST_ID: self.merge_request_id,
                 StringKeyUtils.STR_KEY_IID: self.iid,
                 StringKeyUtils.STR_KEY_ID: self.id,
                 StringKeyUtils.STR_KEY_SHA: self.sha}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = Pipelines()
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.iid = src.get(StringKeyUtils.STR_KEY_IID, None)
                res.sha = src.get(StringKeyUtils.STR_KEY_SHA, None)

            return res

    class parserV4(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = Pipelines()
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.iid = src.get(StringKeyUtils.STR_KEY_IID, None)
                res.sha = src.get(StringKeyUtils.STR_KEY_SHA, None)

            return res

