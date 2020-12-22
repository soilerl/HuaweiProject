import aiohttp
import asyncio
import json
import pymongo

from datetime import datetime

import source.utils.ApiUtils as ApiUtils
import analyzeData.common as common

from source.utils.StringKeyUtils import StringKeyUtils
from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.config.configPraser import configPraser
from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.database.mongoDB.MongoUtil import singleton


class AsyncGetProjectInformationHelper:

    #一页里含有的mergeRequest的数量
    numberOfMergeRequestInOnePage = 20

    def __init__(self, pageIndex='', timeTuple=()):
        self.pageIndex =pageIndex
        #时间限制元组
        self.timeTuple = timeTuple
        #判断是否应该停止爬取mergeRequest列表
        self.shouldFinish = False


    #获取项目一页的MergeRequest的信息
    def getOnePageMergeRequestDataOfProject(self, projectId, mergeRequestIidList=[]):
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(self.preProcess(projectId, mergeRequestIidList))]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

    async def preProcess(self, repo_id, mergeRequestIidList=[]):
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        tasks = [asyncio.ensure_future(self.downloadInformation(repo_id, semaphore, mergeRequestIidList))]
        await asyncio.wait(tasks)

    #下载数据并写入数据库
    async def downloadInformation(self, repo_id, semaphore, mergeRequestIidList=[]):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = self.getOnePageMergeRequestApi(repo_id)
                jsonList = await ApiUtils.fetchData(session, api)
                idList = self.selectTimeSuitMergeRequest(jsonList)
                mergeRequestIidList.extend(idList)

    def getOnePageMergeRequestApi(self, repo_id):
        #默认按照created_at排序
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_REQUESTS + \
              "?scope=all&state=all&page=" + self.pageIndex
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, repo_id)
        return api

    #选择列表里符合时间限制的mergeRequest
    def selectTimeSuitMergeRequest(self, mergeRequestList=[]) -> []:
        resIdList = []
        for mergeRequest in mergeRequestList:
            time = common.tranformStrToDateTime(mergeRequest[StringKeyUtils.STR_KEY_CREATE_AT])
            if common.checkTime(time, self.timeTuple):
                resIdList.append((mergeRequest[StringKeyUtils.STR_KEY_IID], time))
            # else:
            #     if common.che
        return resIdList
if __name__ == '__main__':
    getParameterHelper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos") #
    projectID = getParameterHelper.getProjectID()
    pages = getParameterHelper.getMergeRequestPages()
    mergeRequestIidList = []
    for i in range(1, pages+1):
        helper = AsyncGetProjectInformationHelper(str(i), (2020, 9, 2020, 10))
        helper.getOnePageMergeRequestDataOfProject(projectID)
    for iid in mergeRequestIidList:
        print(iid)
