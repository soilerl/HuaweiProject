#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/7 18:23
# @Author : NJU
# @Version：V 0.1
# @File : Notes.py
# @desc :


from source.data.bean.Beanbase import BeanBase
from source.data.bean.Position import Position
from source.data.bean.User import User
from source.utils.StringKeyUtils import StringKeyUtils


class Notes(BeanBase):
    """ gitlab 数据  notes 数据 共计10个

    """

    def __init__(self):
        self.id = None
        self.type = None
        self.body = None
        self.author = None  # 作者对象的引用
        self.created_at = None
        self.updated_at = None
        self.system = None
        self.noteable_id = None
        self.noteable_type = None
        self.position = None  # position 对象引用
        self.noteable_iid = None

        self.author_user_name = None
        self.change_trigger = None

    @staticmethod
    def getIdentifyKeys():
        items = [StringKeyUtils.STR_KEY_ID]
        return items

    @staticmethod
    def getItemKeyList():
        items = [StringKeyUtils.STR_KEY_ID, StringKeyUtils.STR_KEY_TYPE,
                 StringKeyUtils.STR_KEY_BODY, StringKeyUtils.STR_KEY_AUTHOR_USER_NAME,
                 StringKeyUtils.STR_KEY_CREATE_AT, StringKeyUtils.STR_KEY_UPDATE_AT,
                 StringKeyUtils.STR_KEY_SYSTEM, StringKeyUtils.STR_KEY_NOTEABLE_ID,
                 StringKeyUtils.STR_KEY_NOTEABLE_TYPE, StringKeyUtils.STR_KEY_NOTEABLE_IID,
                 StringKeyUtils.STR_KEY_CHANGE_TRIGGER]

        return items

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_TYPE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_BODY, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_AUTHOR_USER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CREATE_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_UPDATE_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_SYSTEM, BeanBase.DATA_TYPE_BOOLEAN),
                 (StringKeyUtils.STR_KEY_NOTEABLE_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_NOTEABLE_TYPE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_NOTEABLE_IID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_CHANGE_TRIGGER, BeanBase.DATA_TYPE_INT)]

        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_ID : self.id, StringKeyUtils.STR_KEY_TYPE: self.type,
                 StringKeyUtils.STR_KEY_BODY: self.body, StringKeyUtils.STR_KEY_AUTHOR_USER_NAME: self.author_user_name,
                 StringKeyUtils.STR_KEY_CREATE_AT: self.created_at, StringKeyUtils.STR_KEY_UPDATE_AT: self.updated_at,
                 StringKeyUtils.STR_KEY_SYSTEM: self.system, StringKeyUtils.STR_KEY_NOTEABLE_ID: self.noteable_id,
                 StringKeyUtils.STR_KEY_NOTEABLE_TYPE: self.noteable_type,
                 StringKeyUtils.STR_KEY_NOTEABLE_IID: self.noteable_iid,
                 StringKeyUtils.STR_KEY_CHANGE_TRIGGER: self.change_trigger}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = Notes()
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.type = src.get(StringKeyUtils.STR_KEY_TYPE, None)
                res.body = src.get(StringKeyUtils.STR_KEY_BODY, None)
                """解析用户"""
                """分析author"""
                authorUserData = src.get(StringKeyUtils.STR_KEY_AUTHOR, None)
                if authorUserData is not None and isinstance(authorUserData, dict):
                    user = User.parser.parser(authorUserData)
                    res.author = user
                    res.author_user_name = user.username

                res.created_at = src.get(StringKeyUtils.STR_KEY_CREATE_AT, None)
                res.updated_at = src.get(StringKeyUtils.STR_KEY_UPDATE_AT, None)
                res.system = src.get(StringKeyUtils.STR_KEY_SYSTEM, None)
                res.noteable_id = src.get(StringKeyUtils.STR_KEY_NOTEABLE_ID, None)
                res.noteable_type = src.get(StringKeyUtils.STR_KEY_NOTEABLE_TYPE, None)
                """解析position"""
                positionData = src.get(StringKeyUtils.STR_KEY_POSITION, None)
                if positionData is not None and isinstance(positionData, dict):
                    position = Position.parser.parser(positionData)
                    res.position = position
                    position.notes_id = res.id


                res.noteable_iid = src.get(StringKeyUtils.STR_KEY_NOTEABLE_IID, None)

            return res
