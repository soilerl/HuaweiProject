#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/6 23:30
# @Author : NJU
# @Version：V 0.1
# @File : MergeRequest.py
# @desc :
from source.data.bean.Beanbase import BeanBase
from source.data.bean.DiffRefs import DiffRefs
from source.data.bean.User import User
from source.utils.StringKeyUtils import StringKeyUtils


class MergeRequest(BeanBase):
    """记录 Gitlab 的 mergerequest 对象  共计22个
    """

    def __init__(self):
        """声明需要用到的字段"""
        self.repository = None
        self.id = None
        self.iid = None
        self.project_id = None
        self.title = None
        self.description = None
        self.state = None
        self.created_at = None
        self.updated_at = None
        self.merged_by_user = None  # 合入mr的用户的 user 对象引用
        self.merged_at = None
        self.closed_by_user = None  # 关闭mr的用户的 user 对象引用
        self.closed_at = None
        self.target_branch = None
        self.source_branch = None
        self.author = None  # 作者的用户对象引用
        self.source_project_id = None
        self.target_project_id = None
        self.sha = None
        self.merge_commit_sha = None
        self.squash_commit_sha = None
        self.changes_count = None  # MR中涉及的文件改动块
        self.diff_refs = None  # diff_refs 对象引用，作用暂时不明

        """新增字段标识MR修改状态"""
        self.additions = None
        self.changes = None
        self.deletions = None
        self.file_count = None

        """下面放之前引用对象的标识符作为外键"""
        self.merged_by_user_name = None
        self.closed_by_user_name = None
        self.author_user_name = None
        """diff_refs 来拼接MR，所以MR不留diff_refs的标识"""

    @staticmethod
    def getIdentifyKeys():
        """提供对象所有要放数据库的主键"""
        return [StringKeyUtils.STR_KEY_IID, StringKeyUtils.STR_KEY_PROJECT_ID]

    @staticmethod
    def getItemKeyList():
        """提供对象所有要放数据库的数据项"""
        return [StringKeyUtils.STR_KEY_REPOSITORY, StringKeyUtils.STR_KEY_ID,
                StringKeyUtils.STR_KEY_IID, StringKeyUtils.STR_KEY_PROJECT_ID,
                StringKeyUtils.STR_KEY_TITLE, StringKeyUtils.STR_KEY_DESCRIPTION,
                StringKeyUtils.STR_KEY_STATE, StringKeyUtils.STR_KEY_CREATE_AT,
                StringKeyUtils.STR_KEY_UPDATE_AT, StringKeyUtils.STR_KEY_MERGED_BY_USER_NAME,
                StringKeyUtils.STR_KEY_MERGED_AT, StringKeyUtils.STR_KEY_CLOSED_BY_USER_NAME,
                StringKeyUtils.STR_KEY_CLOSED_AT,
                StringKeyUtils.STR_KEY_TARGET_BRANCH, StringKeyUtils.STR_KEY_SOURCE_BRANCH,
                StringKeyUtils.STR_KEY_AUTHOR_USER_NAME, StringKeyUtils.STR_KEY_SOURCE_PROJECT_ID,
                StringKeyUtils.STR_KEY_TARGET_PROJECT_ID, StringKeyUtils.STR_KEY_SHA,
                StringKeyUtils.STR_KEY_MERGE_COMMIT_SHA, StringKeyUtils.STR_KEY_SQUASH_COMMIT_SHA,
                StringKeyUtils.STR_KEY_CHANGES_COUNT, StringKeyUtils.STR_KEY_ADDITIONS,
                StringKeyUtils.STR_KEY_CHANGES, StringKeyUtils.STR_KEY_DELETIONS,
                StringKeyUtils.STR_KEY_FILE_COUNT]

    @staticmethod
    def getItemKeyListWithType():
        items = [(StringKeyUtils.STR_KEY_REPOSITORY, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_IID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_PROJECT_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_TITLE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_DESCRIPTION, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_STATE, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CREATE_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_UPDATE_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_MERGED_BY_USER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_MERGED_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CLOSED_BY_USER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CLOSED_AT, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_TARGET_BRANCH, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_SOURCE_BRANCH, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_AUTHOR_USER_NAME, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_SOURCE_PROJECT_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_TARGET_PROJECT_ID, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_SHA, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_MERGE_COMMIT_SHA, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_SQUASH_COMMIT_SHA, BeanBase.DATA_TYPE_STRING),
                 (StringKeyUtils.STR_KEY_CHANGES_COUNT, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_ADDITIONS, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_CHANGES, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_DELETIONS, BeanBase.DATA_TYPE_INT),
                 (StringKeyUtils.STR_KEY_FILE_COUNT, BeanBase.DATA_TYPE_INT)]
        return items

    def getValueDict(self):
        items = {StringKeyUtils.STR_KEY_REPOSITORY: self.repository,
                 StringKeyUtils.STR_KEY_ID: self.id,
                 StringKeyUtils.STR_KEY_IID: self.iid,
                 StringKeyUtils.STR_KEY_PROJECT_ID: self.project_id,
                 StringKeyUtils.STR_KEY_TITLE: self.title,
                 StringKeyUtils.STR_KEY_DESCRIPTION: self.description,
                 StringKeyUtils.STR_KEY_STATE: self.state,
                 StringKeyUtils.STR_KEY_CREATE_AT: self.created_at,
                 StringKeyUtils.STR_KEY_UPDATE_AT: self.updated_at,
                 StringKeyUtils.STR_KEY_MERGED_BY_USER_NAME: self.merged_by_user_name,
                 StringKeyUtils.STR_KEY_MERGED_AT: self.merged_at,
                 StringKeyUtils.STR_KEY_CLOSED_BY_USER_NAME: self.closed_by_user_name,
                 StringKeyUtils.STR_KEY_CLOSED_AT: self.closed_at,
                 StringKeyUtils.STR_KEY_TARGET_BRANCH: self.target_branch,
                 StringKeyUtils.STR_KEY_SOURCE_BRANCH: self.source_branch,
                 StringKeyUtils.STR_KEY_AUTHOR_USER_NAME: self.author_user_name,
                 StringKeyUtils.STR_KEY_SOURCE_PROJECT_ID: self.source_project_id,
                 StringKeyUtils.STR_KEY_TARGET_PROJECT_ID: self.target_project_id,
                 StringKeyUtils.STR_KEY_SHA: self.sha,
                 StringKeyUtils.STR_KEY_MERGE_COMMIT_SHA: self.merge_commit_sha,
                 StringKeyUtils.STR_KEY_SQUASH_COMMIT_SHA: self.squash_commit_sha,
                 StringKeyUtils.STR_KEY_CHANGES_COUNT: self.changes_count,
                 StringKeyUtils.STR_KEY_ADDITIONS: self.additions,
                 StringKeyUtils.STR_KEY_CHANGES: self.changes,
                 StringKeyUtils.STR_KEY_DELETIONS: self.deletions,
                 StringKeyUtils.STR_KEY_FILE_COUNT: self.file_count}

        return items

    class parser(BeanBase.parser):

        @staticmethod
        def parser(src):
            res = None
            if isinstance(src, dict):
                res = MergeRequest()
                res.id = src.get(StringKeyUtils.STR_KEY_ID, None)
                res.iid = src.get(StringKeyUtils.STR_KEY_IID, None)
                res.project_id = src.get(StringKeyUtils.STR_KEY_PROJECT_ID, None)
                res.title = src.get(StringKeyUtils.STR_KEY_TITLE, None)
                res.description = src.get(StringKeyUtils.STR_KEY_DESCRIPTION, None)
                res.state = src.get(StringKeyUtils.STR_KEY_STATE, None)
                res.created_at = src.get(StringKeyUtils.STR_KEY_CREATE_AT, None)
                res.updated_at = src.get(StringKeyUtils.STR_KEY_UPDATE_AT, None)
                """分析 merged by"""
                mergedByUserData = src.get(StringKeyUtils.STR_KEY_MERGED_BY, None)
                if mergedByUserData is not None and isinstance(mergedByUserData, dict):
                    user = User.parser.parser(mergedByUserData)
                    res.merged_by_user = user
                    res.merged_by_user_name = user.username

                res.merged_at = src.get(StringKeyUtils.STR_KEY_MERGED_AT, None)
                """分析closed by"""
                closedByUserData = src.get(StringKeyUtils.STR_KEY_CLOSED_BY, None)
                if closedByUserData is not None and isinstance(closedByUserData, dict):
                    user = User.parser.parser(closedByUserData)
                    res.closed_by_user = user
                    res.closed_by_user_name = user.username

                res.closed_at = src.get(StringKeyUtils.STR_KEY_CLOSED_AT, None)
                res.target_branch = src.get(StringKeyUtils.STR_KEY_TARGET_BRANCH, None)
                res.source_branch = src.get(StringKeyUtils.STR_KEY_SOURCE_BRANCH, None)

                """分析author"""
                authorUserData = src.get(StringKeyUtils.STR_KEY_AUTHOR, None)
                if authorUserData is not None and isinstance(authorUserData, dict):
                    user = User.parser.parser(authorUserData)
                    res.author = user
                    res.author_user_name = user.username

                res.source_project_id = src.get(StringKeyUtils.STR_KEY_SOURCE_PROJECT_ID, None)
                res.target_project_id = src.get(StringKeyUtils.STR_KEY_TARGET_PROJECT_ID, None)
                res.sha = src.get(StringKeyUtils.STR_KEY_SHA, None)
                res.merge_commit_sha = src.get(StringKeyUtils.STR_KEY_MERGE_COMMIT_SHA, None)
                res.squash_commit_sha = src.get(StringKeyUtils.STR_KEY_SQUASH_COMMIT_SHA, None)
                res.changes_count = src.get(StringKeyUtils.STR_KEY_CHANGES_COUNT, None)

                """分析diff_refs"""
                diffRefsData = src.get(StringKeyUtils.STR_KEY_DIFF_REFS, None)
                if diffRefsData is not None and isinstance(diffRefsData, dict):
                    diff_refs = DiffRefs.parser.parser(diffRefsData)
                    """diff_refs 部分属性需要外部添加"""
                    diff_refs.project_id = res.project_id
                    diff_refs.iid = res.iid
                    res.diff_refs = diff_refs
            return res
