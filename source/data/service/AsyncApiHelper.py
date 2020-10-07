# coding=gbk
import asyncio
import difflib
import json
import random
import time
import traceback
from datetime import datetime

import aiohttp

from source.config.configPraser import configPraser

from source.data.bean.Commits import Commits
from source.data.bean.Diff import Diff
from source.data.bean.MergeRequest import MergeRequest
from source.data.bean.Notes import Notes
from source.data.bean.Position import Position
from source.data.service.AsyncSqlHelper import AsyncSqlHelper
from source.data.service.GraphqlHelper import GraphqlHelper
from source.data.service.ProxyHelper import ProxyHelper
from source.data.service.TextCompareUtils import TextCompareUtils
from source.utils.Logger import Logger
from source.utils.StringKeyUtils import StringKeyUtils


class AsyncApiHelper:
    """使用aiohttp异步通讯"""

    owner = None
    repo = None
    repo_id = None

    @staticmethod
    def setRepo(owner, repo):  # 使用之前设置项目名和所有者
        AsyncApiHelper.owner = owner
        AsyncApiHelper.repo = repo

    @staticmethod
    def setRepoId(repo_id):  # GitLab需要在使用前设置项目的id
        AsyncApiHelper.repo_id = repo_id

    @staticmethod
    def getAuthorizationHeaders(header):
        """设置Github 的Token用于验证"""
        if header is not None and isinstance(header, dict):
            if configPraser.getAuthorizationToken():
                header[StringKeyUtils.STR_HEADER_AUTHORIZAITON] = (StringKeyUtils.STR_HEADER_TOKEN
                                                                   + configPraser.getAuthorizationToken())
        return header

    @staticmethod
    def getPrivateTokensHeaders(header):
        """设置Gitlab 的Token用于验证"""
        if header is not None and isinstance(header, dict):
            if configPraser.getAuthorizationToken():
                header[StringKeyUtils.STR_HEADER_PRIVATE_TOKEN] = (configPraser.getPrivateToken())
        return header

    @staticmethod
    def getUserAgentHeaders(header):
        """爬虫策略： 随机请求的agent"""
        if header is not None and isinstance(header, dict):
            # header[self.STR_HEADER_USER_AGENT] = self.STR_HEADER_USER_AGENT_SET
            header[StringKeyUtils.STR_HEADER_USER_AGENT] = random.choice(StringKeyUtils.USER_AGENTS)
        return header

    @staticmethod
    def getMediaTypeHeaders(header):
        if header is not None and isinstance(header, dict):
            header[StringKeyUtils.STR_HEADER_ACCEPT] = StringKeyUtils.STR_HEADER_MEDIA_TYPE
        return header

    @staticmethod
    async def getProxy():
        """获取代理ip池中的ip  详细看 ProxyHelper"""
        if configPraser.getProxy():
            proxy = await ProxyHelper.getAsyncSingleProxy()
            if configPraser.getPrintMode():
                print(proxy)
            if proxy is not None:
                return StringKeyUtils.STR_PROXY_HTTP_FORMAT.format(proxy)
        return None

    @staticmethod
    async def parserMergeRequest(resultJson):
        try:
            res = None
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    res = MergeRequest.parser.parser(resultJson)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL接口解析可能会不大一样
            if res is not None:
                res.repository = AsyncApiHelper.owner + '/' + AsyncApiHelper.repo
                return res
        except Exception as e:
            print(e)

    @staticmethod
    async def parserNotes(resultJson):
        try:
            resList = []
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    if resultJson is not None and isinstance(resultJson, list):
                        for notesData in resultJson:
                            notes = Notes.parser.parser(notesData)
                            if notes is not None:
                                resList.append(notes)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL接口解析可能会不大一样
            return resList
        except Exception as e:
            print(e)

    @staticmethod
    async def parserCommit(resultJson):
        try:
            resList = []
            if configPraser.getApiVersion() == StringKeyUtils.API_VERSION_RESET:
                if not AsyncApiHelper.judgeNotFind(resultJson):
                    if resultJson is not None and isinstance(resultJson, list):
                        for commitData in resultJson:
                            commit = Commits.parser.parser(commitData)
                            if commit is not None:
                                resList.append(commit)
            elif configPraser.getApiVersion() == StringKeyUtils.API_VERSION_GRAPHQL:
                pass
                # GraphQL接口解析可能会不大一样
            return resList
        except Exception as e:
            print(e)

    @staticmethod
    def judgeNotFind(resultJson):
        if resultJson is not None and isinstance(json, dict):
            if resultJson.get(StringKeyUtils.STR_KEY_MESSAGE) == StringKeyUtils.STR_NOT_FIND:
                return True
            if resultJson.get(StringKeyUtils.STR_KEY_MESSAGE) == StringKeyUtils.STR_FAILED_FETCH:
                return True
        return False

    @staticmethod
    def judgeNotFindV4(resultJson):
        """v4 接口的not find判断和v3的不大相同"""
        if resultJson is not None and isinstance(json, dict):
            if resultJson.get(StringKeyUtils.STR_KEY_ERRORS) is not None:
                return True
        return False

    @staticmethod
    async def judgeChangeTrigger(session, pr_author, change_sha, notes):
        position = notes.position
        if position is not None and isinstance(position, Position):
            head_sha = position.head_sha
            username = notes.author_user_name
            if username == pr_author:
                notes.change_trigger = -2  # -2 代表作者自己发言
                return
            diffs = await AsyncApiHelper.getDiffBetweenCommits(session, head_sha, change_sha)
            if diffs is not None and isinstance(diffs, list):
                for diffData in diffs:
                    diff = Diff.parser.parser(diffData)
                    if diff is not None:
                        if diff.new_path == notes.position.new_path or diff.old_path == notes.position.old_path:
                            print(diff.diff)
                            """解析diff hunk"""
                            TextCompareUtils.patchParser(diff.diff)


    @staticmethod
    def urlAppendParams(url, paramsDict):
        isFirst = True
        for k, v in paramsDict.items():
            if isFirst:
                url += f'?{k}={v}'
                isFirst = False
            else:
                url += f'&{k}={v}'
        return url

    @staticmethod
    async def getDiffBetweenCommits(session, sha1, sha2):
        api = AsyncApiHelper.getCommitCompareApi()
        api = AsyncApiHelper.urlAppendParams(api, {'from': sha1, 'to': sha2})
        json = await AsyncApiHelper.fetchBeanData(session, api)
        if json is not None and isinstance(json, dict):
            return json.get(StringKeyUtils.STR_KEY_DIFFS, None)

    @staticmethod
    async def downloadInformation(merge_request_iid, semaphore, mysql, statistic):
        """获取一个项目 单个merge-request 相关的信息"""

        """增加issue  需要仿写downloadInformation函数 
           只是pull-request的获取转换为issue
        """
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                try:
                    beanList = []  # 用来收集需要存储的bean类
                    """先获取pull request信息"""
                    api = AsyncApiHelper.getMergeRequestApi(merge_request_iid)
                    json = await AsyncApiHelper.fetchBeanData(session, api)
                    print(json)
                    merge_request = await AsyncApiHelper.parserMergeRequest(json)
                    print(merge_request)
                    usefulMergeRequestsCount = 0

                    if merge_request is not None:
                        usefulMergeRequestsCount = 1
                        """需要配保存数据库的对象放入beanList即可"""
                        beanList.append(merge_request)

                        if merge_request.diff_refs is not None:
                            beanList.append(merge_request.diff_refs)
                        if merge_request.author is not None:
                            beanList.append(merge_request.author)
                        if merge_request.merged_by_user is not None:
                            beanList.append(merge_request.merged_by_user)
                        if merge_request.closed_by_user is not None:
                            beanList.append(merge_request.closed_by_user)

                        pr_author = merge_request.author_user_name

                        """获取commits"""
                        api = AsyncApiHelper.getCommitApi(merge_request_iid)
                        json = await AsyncApiHelper.fetchBeanData(session, api)
                        print(json)
                        commitList = []
                        if json is not None and isinstance(json, list):
                            commitList = await AsyncApiHelper.parserCommit(json)

                        """获取notes"""
                        api = AsyncApiHelper.getNotesApi(merge_request_iid)
                        json = await AsyncApiHelper.fetchBeanData(session, api)
                        print(json)

                        """获取第一个commit的sha"""
                        change_sha = commitList[0].id

                        nodesList = []
                        if json is not None and isinstance(json, list):
                            nodesList = await AsyncApiHelper.parserNotes(json)

                        # """分析评论"""
                        # for nodes in nodesList:
                        #     if nodes.position is not None:
                        #         await AsyncApiHelper.judgeChangeTrigger(session, pr_author, change_sha, nodes)

                        print(beanList)

                    """数据库存储"""
                    await AsyncSqlHelper.storeBeanDateList(beanList, mysql)

                    # 做了同步处理
                    statistic.lock.acquire()
                    statistic.usefulRequestNumber += usefulMergeRequestsCount
                    """有了其他数据同样可以做统计"""

                    print("useful pull request:", statistic.usefulRequestNumber,
                          " useful review:", statistic.usefulReviewNumber,
                          " useful review comment:", statistic.usefulReviewCommentNumber,
                          " useful issue comment:", statistic.usefulIssueCommentNumber,
                          " useful commit:", statistic.usefulCommitNumber,
                          " cost time:", datetime.now() - statistic.startTime)
                    statistic.lock.release()
                except Exception as e:
                    print(e)

    @staticmethod
    def getGraphQLApi():
        api = StringKeyUtils.API_GITHUB + StringKeyUtils.API_GRAPHQL
        return api

    @staticmethod
    def getMergeRequestApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_PULL_REQUEST
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    def getCommitCompareApi():
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS_COMPARE
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        return api

    @staticmethod
    def getNotesApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_NOTES
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    def getCommitApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    async def fetchBeanData(session, api, isMediaType=False):
        """异步获取数据通用接口（重要）"""

        """初始化请求头"""
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getPrivateTokensHeaders(headers)  # 现在用token好似有点问题 先注释掉 2020.10.7

        while True:
            """对单个请求循环判断 直到请求成功或者错误"""

            """获取代理ip  ip获取需要运行代理池"""
            proxy = await AsyncApiHelper.getProxy()
            if configPraser.getProxy() and proxy is None:  # 对代理池没有ip的情况做考虑
                print('no proxy and sleep!')
                await asyncio.sleep(20)
            else:
                break

        try:
            async with session.get(api, ssl=False, proxy=proxy
                    , headers=headers, timeout=configPraser.getTimeout()) as response:
                print("rate:", response.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
                print("status:", response.status)
                if response.status == 403:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_KILL_POINT)
                    raise 403
                elif proxy is not None:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_POSITIVE_POINT)
                return await response.json()
        except Exception as e:
            """非 403的网络请求出错  循环重试"""
            print(e)
            if proxy is not None:
                proxy = proxy.split('//')[1]
                await ProxyHelper.judgeProxy(proxy, ProxyHelper.INT_NEGATIVE_POINT)
            # print("judge end")
            """循环重试"""
            return await AsyncApiHelper.fetchBeanData(session, api, isMediaType=isMediaType)

    @staticmethod
    async def postGraphqlData(session, api, query=None, args=None):
        """通过 github graphhql接口 通过post请求"""
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getAuthorizationHeaders(headers)

        body = {}
        body = GraphqlHelper.getGraphlQuery(body, query)
        body = GraphqlHelper.getGraphqlVariables(body, args)
        bodyJson = json.dumps(body)
        # print("bodyjson:", bodyJson)

        while True:
            proxy = await AsyncApiHelper.getProxy()
            if configPraser.getProxy() and proxy is None:  # 对代理池没有ip的情况做考虑
                print('no proxy and sleep!')
                await asyncio.sleep(20)
            else:
                break

        try:
            async with session.post(api, ssl=False, proxy=proxy,
                                    headers=headers, timeout=configPraser.getTimeout(),
                                    data=bodyJson) as response:
                print("rate:", response.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
                print("status:", response.status)
                if response.status == 403:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_KILL_POINT)
                    raise 403
                elif proxy is not None:
                    await ProxyHelper.judgeProxy(proxy.split('//')[1], ProxyHelper.INT_POSITIVE_POINT)
                return await response.json()
        except Exception as e:
            print(e)
            if proxy is not None:
                proxy = proxy.split('//')[1]
                await ProxyHelper.judgeProxy(proxy, ProxyHelper.INT_NEGATIVE_POINT)
            print("judge end")
            return await AsyncApiHelper.postGraphqlData(session, api, query, args)
