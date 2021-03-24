# _*_ coding: utf-8 _*_
import asyncio
import difflib
import json
import os
import random
import time
import traceback
from datetime import datetime

import aiohttp
from pandas import DataFrame

from source.config.configPraser import configPraser
from source.config.projectConfig import projectConfig

from source.data.bean.Commits import Commits
from source.data.bean.Diff import Diff
from source.data.bean.Discussions import Discussions
from source.data.bean.MergeRequest import MergeRequest
from source.data.bean.Notes import Notes
from source.data.bean.Pipelines import Pipelines
from source.data.bean.Position import Position
from source.data.service.BeanStoreHelper import BeanStoreHelper
from source.data.service.GraphqlHelper import GraphqlHelper
from source.data.service.NoteAnalyser import NoteAnalyser
from source.data.service.ProxyHelper import ProxyHelper
from source.data.service.TextCompareUtils import TextCompareUtils
from source.utils.StringKeyUtils import StringKeyUtils


class AsyncApiHelper:
    """使用aiohttp异步通讯"""

    owner = None
    repo = None
    repo_id = None
    mr_num = 0  # 如果获取了某个项目的merge request的最大数量，放在这里 2020.12.21
    projectList = None  # 用于存放某个group的项目

    @staticmethod
    def setRepo(owner, repo):  # 使用之前设置项目名和所有者
        AsyncApiHelper.owner = owner
        AsyncApiHelper.repo = repo

    @staticmethod
    def setRepoId(repo_id):  # GitLab需要在使用前设置项目的id
        AsyncApiHelper.repo_id = repo_id

    @staticmethod
    def getAuthorizationHeaders(header):
        """设置Gitlub 的Token用于验证"""
        if header is not None and isinstance(header, dict):
            if configPraser.getPrivateToken():
                header[StringKeyUtils.STR_HEADER_AUTHORIZAITON] = (StringKeyUtils.STR_HEADER_BEARER
                                                                   + configPraser.getPrivateToken())
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
    def getContentTypeHeaders(header):
        if header is not None and isinstance(header, dict):
            header[StringKeyUtils.STR_HEADER_CONTENT_TYPE] = StringKeyUtils.STR_HEADER_APPLICATION
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

            """暂时做一个近似"""
            if position.new_line is None and position.old_line is not None:
                position.new_line = position.old_line

            notes.change_trigger = -1

            diffs = await AsyncApiHelper.getDiffBetweenCommits(session, head_sha, change_sha)
            if diffs is not None and isinstance(diffs, list):
                for diffData in diffs:
                    diff = Diff.parser.parser(diffData)
                    if diff is not None:
                        if diff.new_path == notes.position.new_path or diff.old_path == notes.position.old_path:
                            print(diff.diff)
                            """解析diff hunk"""
                            textChanges = TextCompareUtils.patchParser(diff.diff)

                            dis = 10000000
                            """依次遍历每个patch 找到每个patch 中距离 original_line 最进的改动距离"""
                            for textChange in textChanges:
                                start_left, _, start_right, _ = textChange[0]
                                status = textChange[1]
                                """curPos 选取 left， 因为对于变动，comment 的行数属于老版本"""
                                curPos = start_left - 1
                                for s in status:
                                    if s != '+':
                                        curPos += 1
                                    if s == '+' or s == '-':
                                        dis = min(dis, abs(position.new_line - curPos))
                            if dis <= 10:
                                if notes.change_trigger == -1:
                                    notes.change_trigger = dis
                                else:
                                    notes.change_trigger = min(notes.change_trigger, dis)
                            else:
                                if notes.change_trigger == -1:
                                    notes.change_trigger = -1

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
        api = AsyncApiHelper.urlAppendParams(api, {'from': sha1, 'to': sha2, 'straight': True})
        json = await AsyncApiHelper.fetchBeanData(session, api)
        if json is not None and isinstance(json, dict):
            return json.get(StringKeyUtils.STR_KEY_DIFFS, None)

    @staticmethod
    async def fetchMergeRequestNum(semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = AsyncApiHelper.getMergeRequestListApi()
                json = await AsyncApiHelper.fetchBeanData(session, api)
                print(json)
                if json is not None and isinstance(json, list):
                    if json.__len__() > 0:
                        """取第一个，第一个就是最新的mr"""
                        merge_request = await AsyncApiHelper.parserMergeRequest(json[0])
                        AsyncApiHelper.mr_num = merge_request.iid

    @staticmethod
    async def fetchProjectsByGroup(semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = AsyncApiHelper.getGroupApi()
                json = await AsyncApiHelper.fetchBeanData(session, api)
                print(json)
                projectList = []
                if json is not None and isinstance(json, dict):
                    projectsData = json.get(StringKeyUtils.STR_KEY_PROJECTS)
                    if projectsData is not None and isinstance(projectsData, list):
                        for data in projectsData:
                            project_id = data.get(StringKeyUtils.STR_KEY_ID, None)
                            project_name = data.get(StringKeyUtils.STR_KEY_PATH, None)
                            projectList.append((AsyncApiHelper.owner, project_name, project_id))
                AsyncApiHelper.projectList = projectList


    @staticmethod
    async def downloadInformation(merge_request_iid, semaphore, statistic):
        """获取一个项目 单个merge-request 相关的信息"""

        """增加issue  需要仿写downloadInformation函数 
           只是pull-request的获取转换为issue
        """
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                try:
                    beanList = []
                    api = AsyncApiHelper.getMergeRequestApi(merge_request_iid)
                    json = await AsyncApiHelper.fetchBeanData(session, api)
                    print(merge_request_iid, "获取失败")
                    if json == None or json == '':
                        return
                    print(json)
                    merge_request = await AsyncApiHelper.parserMergeRequest(json)
                    print(merge_request)
                    usefulMergeRequestsCount = 0

                    if merge_request is not None:
                        usefulMergeRequestsCount = 1
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

                        api = AsyncApiHelper.getCommitApi(merge_request_iid)
                        json = await AsyncApiHelper.fetchBeanData(session, api)
                        print(json)
                        commitList = []
                        if json is not None and isinstance(json, list):
                            commitList = await AsyncApiHelper.parserCommit(json)

                        change_sha = commitList[0].id

                        page_index = 1
                        nodesList = []
                        isMorePage = True
                        while isMorePage:
                            api = AsyncApiHelper.getNotesApi(merge_request_iid, page_index)
                            json = await AsyncApiHelper.fetchBeanData(session, api)
                            print(json)
                            if json is not None and isinstance(json, list):
                                nodesList.extend(await AsyncApiHelper.parserNotes(json))
                                if (json.__len__()) < 20:
                                    isMorePage = False
                                else:
                                    page_index += 1
                            else:
                                isMorePage = False
                        for nodes in nodesList:
                            nodes.merge_request_id = merge_request_iid
                            if nodes.position is not None:
                                await AsyncApiHelper.judgeChangeTrigger(session, pr_author, change_sha, nodes)
                                # beanList.append(nodes)

                        print(beanList)

                        comments = [notes for notes in nodesList if notes.position is not None]
                        """存储notes 这里存储的notes需要保证只有代码评审"""
                        if comments is not None and isinstance(comments, list):
                            notesFileName = projectConfig.getNotesDataPath() + os.sep + \
                                            f"notes_{AsyncApiHelper.repo}.tsv"
                            BeanStoreHelper.storeBeansToTSV(comments, notesFileName)

                        mergeRequestFileName = projectConfig.getMergeRequestDataPath() + os.sep + \
                                               f"mergeRequest_{AsyncApiHelper.repo}.tsv"
                        BeanStoreHelper.storeBeansToTSV([merge_request], mergeRequestFileName)

                    statistic.lock.acquire()
                    statistic.usefulRequestNumber += usefulMergeRequestsCount

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
    async def analysisChangeTrigger(session, notes, discussions, pipelines, author):
        """通过notes
           来分析代码评审的评论是否触发变更
        """
        """先遍历notes 做深层分析"""
        tempList = []
        for note in notes:
            """对notes类型识别"""
            NoteAnalyser.analysisSingleNote(note)
        for index, note in enumerate(notes):
            print("index", index, "  type:", note.notesType, "  ", note.commit_sha)

        """notes倒序 切分成不同commit 和  discussion 片段"""
        notes.reverse()

        timeLineList = []  # 用于存放不同的 discussion和 commit

        for note in notes:
            if isinstance(note, Notes):
                if note.notesType == Notes.STR_KEY_OTHER:
                    """不感兴趣对象直接过滤"""
                    continue
                elif note.notesType == Notes.STR_KEY_INLINE_COMMENT:
                    """用户评论"""
                    note.change_trigger = -1
                    """先寻找discussion"""
                    for discussion in discussions:
                        if note.discussion_id == discussion.id:
                            if discussion.analysisNodesList is None:
                                discussion.analysisNodesList = []
                                timeLineList.append(discussion)
                            discussion.analysisNodesList.append(note)
                elif note.notesType == Notes.STR_KEY_COMMIT:
                    """commit 直接放入"""

                    """现在commit只有8位的sha， 通过pipeline作为辅助，补全sha"""
                    for pipeline in pipelines:
                        if note.commit_sha == pipeline.sha[:8]:
                            note.commit_sha = pipeline.sha
                            break
                    timeLineList.append(note)
                elif note.notesType == Notes.STR_KEY_SYSTEM_CHANGE_NOTICE:
                    """系统提示该表标识  不放入discussion, 但是认为discussion 发生变化"""
                    for discussion in discussions:
                        if note.discussion_id == discussion.id:
                            discussion.change_trigger_system = True

        print(timeLineList)
        """把 discussion 和 commit 切分成不同的小组"""
        review_change_pair = []
        temp_discussions = []  # 用于记录同一大组的 discussion
        temp_commits = []
        for event in timeLineList:
            if isinstance(event, Notes) and event.notesType == Notes.STR_KEY_COMMIT:
                if temp_discussions.__len__() > 0:  # 需要保证commit是在 discussion 后面
                    temp_commits.append(event)
            if isinstance(event, Discussions):
                if temp_commits.__len__() > 0:
                    review_change_pair.append([temp_discussions, temp_commits])
                    temp_discussions = []
                    temp_commits = []
                temp_discussions.append(event)
        """收尾"""
        if temp_discussions.__len__() > 0 and temp_commits.__len__() > 0:
            review_change_pair.append([temp_discussions, temp_commits])

        print(review_change_pair)
        """对每一对 review_change_pair 分析change_trigger"""

        """用于存储计算结束的comment"""
        resultCommentList = []

        for discussions, changes in review_change_pair:
            await AsyncApiHelper.analysisReviewChangePair(session, discussions, changes, author)

        print(discussions)
        for note in notes:
            if note.notesType == Notes.STR_KEY_INLINE_COMMENT:
                resultCommentList.append(note)

        return resultCommentList

    @staticmethod
    async def analysisReviewChangePair(session, discussions, changes, author):

        for discussion in discussions:
            """只能确保每个discussion的第一个comment版本是对的
               如果第一个触发了代码的变更，后面的作为连带的关系，
               统统认为触发了代码的变更
            """
            comment = discussion.analysisNodesList[0]
            review_sha = comment.position.head_sha  # 我们认为代码评审最新的版本，也就是head_sha的版本
            review_line = comment.position.new_line
            review_file = comment.position.new_path  # 一般来说代码评审都是看添加的部分，即new的部分

            if review_line is None:
                review_line = comment.position.old_path  # 否则指向原来的的行数

            change_trigger = -1  # 先认为没触发
            INT_MAX_LINE = 10000000
            for change in changes:
                change_sha = change.commit_sha

                """请求接口获得两个版本的差异"""
                diffs = await AsyncApiHelper.getDiffBetweenCommits(session, review_sha, change_sha)
                if diffs is not None and isinstance(diffs, list):
                    for diffData in diffs:
                        diff = Diff.parser.parser(diffData)
                        if diff is not None:
                            if diff.new_path == review_file or diff.old_path == review_file:
                                print(diff.diff)
                                """解析diff hunk"""
                                textChanges = TextCompareUtils.patchParser(diff.diff)

                                dis = INT_MAX_LINE
                                """依次遍历每个patch 找到每个patch 中距离 original_line 最进的改动距离"""
                                for textChange in textChanges:
                                    start_left, _, start_right, _ = textChange[0]
                                    status = textChange[1]
                                    """curPos 选取 left， 因为对于变动，comment 的行数属于老版本"""
                                    curPos = start_left - 1
                                    for s in status:
                                        if s != '+':
                                            curPos += 1
                                        if s == '+' or s == '-':
                                            dis = min(dis, abs(review_line - curPos))
                                if dis <= 10:
                                    if change_trigger == -1:
                                        change_trigger = dis
                                    else:
                                        change_trigger = min(change_trigger, dis)
                                else:
                                    if change_trigger == -1:
                                        change_trigger = -1
                if change_trigger == 0:
                    break

            """对每个discussion的notes做结算"""
            for note in discussion.analysisNodesList:
                if note.notesType == Notes.STR_KEY_INLINE_COMMENT:
                    if note.author_user_name == author:
                        note.change_trigger = -2
                    else:
                        note.change_trigger = change_trigger

    @staticmethod
    def getGraphQLApi():
        api = StringKeyUtils.API_GITLAB_GRAPHQL
        return api

    # 根据iid获取用于爬取的api
    @staticmethod
    def getMergeRequestApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_PULL_REQUEST
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    # 根据获取某项目的一页mergeRequest列表
    @staticmethod
    def getMergeRequestListApi():
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_PULL_REQUEST_LIST
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        return api

    # 根据获取某group的一页项目列表
    @staticmethod
    def getGroupApi():
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_GROUP
        api = api.replace(StringKeyUtils.STR_OWNER, str(AsyncApiHelper.owner))
        return api

    @staticmethod
    def getCommitCompareApi():
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS_COMPARE
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        return api

    @staticmethod
    def getNotesApi(merge_request_iid, page_index):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_NOTES
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        api = api.replace(StringKeyUtils.STR_PAGE_INDEX, str(page_index))
        return api

    @staticmethod
    def getCommitApi(merge_request_iid):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_COMMITS
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, str(AsyncApiHelper.repo_id))
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, str(merge_request_iid))
        return api

    @staticmethod
    async def fetchBeanData(session, api, isMediaType=False, times = 0):
        """异步获取数据通用接口（重要）"""

        """初始化请求头"""
        headers = {}
        # 设置agent
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        # 设置Token
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
            if times > 5:
                return
            if proxy is not None:
                proxy = proxy.split('//')[1]
                await ProxyHelper.judgeProxy(proxy, ProxyHelper.INT_NEGATIVE_POINT)
            # print("judge end")
            """循环重试"""
            times += 1
            return await AsyncApiHelper.fetchBeanData(session, api, isMediaType=isMediaType, times=times)

    @staticmethod
    async def postGraphqlData(session, api, query=None, args=None):
        """通过 github graphhql接口 通过post请求"""
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getAuthorizationHeaders(headers)
        headers = AsyncApiHelper.getContentTypeHeaders(headers)

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
