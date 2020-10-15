#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/7 16:29
# @Author : NJU
# @Version：V 0.1
# @File : Commits.py
# @desc :
from source.data.bean.Beanbase import BeanBase
from source.utils.StringKeyUtils import StringKeyUtils


class Commits(BeanBase):
    """记录 Gitlab 的 commits 对象  共计17个
    """

    def __init__(self):
        self.id = None
        self.short_id = None
        self.created_at = None
        self.parent_ids = None
        self.title = None
        self.message = None
        self.author_name = None
        self.author_email = None
        self.authored_date = None
        self.committer_name = None
        self.committer_email = None
        self.committer_date = None
        self.web_url = None
        self.stats_additions = None
        self.stats_deletions = None
        self.stats_total = None
        self.status = None
        self.project_id = None

    @staticmethod
    def getIdentifyKeys():
        """提供对象所有要放数据库的主键"""
        return [StringKeyUtils.STR_KEY_IID]

    @staticmethod
    def getItemKeyList():
        """提供对象所有要放数据库的数据项"""
        return [StringKeyUtils.STR_KEY_ID, StringKeyUtils.STR_KEY_SHORT_ID,
                StringKeyUtils.STR_KEY_CREATE_AT, StringKeyUtils.STR_KEY_TITLE,
                StringKeyUtils.STR_KEY_MESSAGE, StringKeyUtils.STR_KEY_AUTHOR_NAME,
                StringKeyUtils.STR_KEY_AUTHOR_EMAIL, StringKeyUtils.STR_KEY_AUTHORED_DATE,
                StringKeyUtils.STR_KEY_COMMITTER_NAME, StringKeyUtils.STR_KEY_COMMITTER_EMAIL,
                StringKeyUtils.STR_KEY_COMMITTER_DATE, StringKeyUtils.STR_KEY_WEB_URL,
                StringKeyUtils.STR_KEY_STATS_ADDITIONS, StringKeyUtils.STR_KEY_STATS_DELETIONS,
                StringKeyUtils.STR_KEY_STATS_TOTAL, StringKeyUtils.STR_KEY_STATUS,
                StringKeyUtils.STR_KEY_PROJECT_ID]

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_SHORT_ID, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CREATE_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_TITLE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_MESSAGE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_AUTHOR_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_AUTHOR_EMAIL, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_AUTHORED_DATE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_COMMITTER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_COMMITTER_EMAIL, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_COMMITTER_DATE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_WEB_URL, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_STATS_ADDITIONS, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_STATS_DELETIONS, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_STATS_TOTAL, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_STATUS, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_PROJECT_ID, BeanBase.DATA_TYPE_INT)]
        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_ID: self.id,
                 StringKeyUtils.STR_KEY_SHORT_ID: self.short_id,
                 StringKeyUtils.STR_KEY_CREATE_AT: self.created_at,
                 StringKeyUtils.STR_KEY_TITLE: self.title,
                 StringKeyUtils.STR_KEY_MESSAGE: self.message,
                 StringKeyUtils.STR_KEY_AUTHOR_NAME: self.author_name,
                 StringKeyUtils.STR_KEY_AUTHOR_EMAIL: self.author_email,
                 StringKeyUtils.STR_KEY_AUTHORED_DATE: self.authored_date,
                 StringKeyUtils.STR_KEY_COMMITTER_NAME: self.committer_name,
                 StringKeyUtils.STR_KEY_COMMITTER_EMAIL: self.committer_email,
                 StringKeyUtils.STR_KEY_COMMITTER_DATE: self.committer_date,
                 StringKeyUtils.STR_KEY_WEB_URL: self.web_url,
                 StringKeyUtils.STR_KEY_STATS_ADDITIONS: self.stats_additions,
                 StringKeyUtils.STR_KEY_STATS_DELETIONS: self.stats_deletions,
                 StringKeyUtils.STR_KEY_STATS_TOTAL: self.stats_total,
                 StringKeyUtils.STR_KEY_STATUS: self.status,
                 StringKeyUtils.STR_KEY_PROJECT_ID: self.project_id}
        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = Commits()
            if isinstance(src, dict):
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.short_id = src.get(StringKeyUtils.STR_KEY_SHORT_ID, None)
                res.created_at = src.get(StringKeyUtils.STR_KEY_CREATE_AT, None)
                res.parent_ids = src.get(StringKeyUtils.STR_KEY_PARENT_IDS, None)
                res.title = src.get(StringKeyUtils.STR_KEY_TITLE, None)
                res.message = src.get(StringKeyUtils.STR_KEY_MESSAGE, None)
                res.author_name = src.get(StringKeyUtils.STR_KEY_AUTHOR_NAME, None)
                res.author_email = src.get(StringKeyUtils.STR_KEY_AUTHOR_EMAIL, None)
                res.authored_date = src.get(StringKeyUtils.STR_KEY_AUTHORED_DATE, None)
                res.committer_name = src.get(StringKeyUtils.STR_KEY_COMMITTER_NAME, None)
                res.committer_email = src.get(StringKeyUtils.STR_KEY_COMMITTER_EMAIL, None)
                res.committer_date = src.get(StringKeyUtils.STR_KEY_COMMITTER_DATE, None)
                res.web_url = src.get(StringKeyUtils.STR_KEY_WEB_URL, None)
                res.stats_additions = src.get(StringKeyUtils.STR_KEY_STATS_ADDITIONS, None)
                res.stats_deletions = src.get(StringKeyUtils.STR_KEY_STATS_DELETIONS, None)
                res.stats_total = src.get(StringKeyUtils.STR_KEY_STATS_TOTAL, None)
                res.status = src.get(StringKeyUtils.STR_KEY_STATUS, None)
                res.project_id = src.get(StringKeyUtils.STR_KEY_PROJECT_ID, None)

            return res
