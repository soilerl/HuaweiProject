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
# from source.database.mongoDB.MongoUtil import singleton


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

    #下载数据
    async def downloadInformation(self, repo_id, semaphore, mergeRequestIidList=[]):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = self.getOnePageMergeRequestApi(repo_id)
                jsonList = await ApiUtils.fetchData(session, api)
                idList = self.selectTimeSuitMergeRequest(jsonList)
                mergeRequestIidList.extend(idList)

<<<<<<< HEAD
    def getOnePageMergeRequestApi(self, repo_id):
        #默认按照created_at排序
=======
    #校验要写入的mergeRequest是否已经存在
    def checkExist(self, mergeRequest={}) -> bool:
        if mergeRequest == None:
            return False
        id = mergeRequest['id']
        # id ==
    def getProjectApi(self, repo_id):
>>>>>>> 15aea558989b1075694541c2255a118662f1d0d7
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
                resIdList.append(mergeRequest[StringKeyUtils.STR_KEY_IID])
            else:
                if common.checkTimeIsLessThan(time, self.timeTuple):
                    self.shouldFinish = True
        return resIdList

    #对外暴露的接口，获取某个项目的符合时间限制的所有mergeRequestIid
    @staticmethod
    def getMergeRequestIidList(url='', timeLimit=()) -> []:
        getParameterHelper = GetInformationOfParameterHelper(url)
        projectID = getParameterHelper.getProjectID()
        pages = getParameterHelper.getMergeRequestPages()
        mergeRequestIidList = []
        for i in range(1, pages + 1):
            helper = AsyncGetProjectInformationHelper(str(i), timeLimit)
            helper.getOnePageMergeRequestDataOfProject(projectID, mergeRequestIidList)
            if helper.shouldFinish:
                break
        return mergeRequestIidList

if __name__ == '__main__':
<<<<<<< HEAD
    arr = AsyncGetProjectInformationHelper.getMergeRequestIidList("https://gitlab.com/tezos/tezos", (2020, 9, 2020, 10))
    for i in arr:
        print(i)
=======
    getParameterHelper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos")
    projectID = getParameterHelper.getProjectID()
    print(projectID)
    # pages = getParameterHelper.getMergeRequestPages()
    # for i in range(1, 3):
    #     helper = AsyncGetProjectInformationHelper(str(i))
    #     helper.getOnePageMergeRequestDataOfProject(projectID)
>>>>>>> 15aea558989b1075694541c2255a118662f1d0d7
