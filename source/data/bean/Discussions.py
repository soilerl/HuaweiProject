#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/8 11:22
# @Author : NJU
# @Version：V 0.1
# @File : Discussions.py
# @desc :

from source.data.bean.Beanbase import BeanBase
from source.data.bean.Notes import Notes
from source.utils.StringKeyUtils import StringKeyUtils


class Discussions(BeanBase):
    """记录 Gitlab 的 discussions 对象
    """

    def __init__(self):
        self.id = None
        self.notes = None  # List

        self.change_trigger_system = None  # 用于标识系统判定的更改
        self.analysisNodesList = None  # 分析时候用的 notes 的暂时存储

    @staticmethod
    def getIdentifyKeys():
        """提供对象所有要放数据库的主键"""
        return [StringKeyUtils.STR_KEY_ID]

    @staticmethod
    def getItemKeyList():
        """提供对象所有要放数据库的数据项"""
        return [StringKeyUtils.STR_KEY_ID]

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_STRING)]
        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_ID: self.id}
        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = Discussions()
            if isinstance(src, dict):
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                notes = src.get(StringKeyUtils.STR_KEY_NOTES, None)
                if notes is not None and isinstance(notes, list):
                    note_list = []
                    for note in notes:
                        if note is not None:
                            note_list.append(Notes.parser.parser(note))
                    res.notes = note_list

            return res

    class parserV4(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = Discussions()
            if isinstance(src, dict):
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                notes = src.get(StringKeyUtils.STR_KEY_NOTES, None)
                if notes is not None and isinstance(notes, dict):
                    notesData = notes.get(StringKeyUtils.STR_KEY_NODES, None)
                    if isinstance(notesData, list):
                        note_list = []
                        for note in notesData:
                            if note is not None:
                                note_list.append(Notes.parserV4.parser(note))
                        res.notes = note_list

            return res
