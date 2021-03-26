import aiohttp
import asyncio
import json
import pymongo
from source.utils import utils as utils

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

    def __init__(self, pageIndex, timeTuple=()):
        self.pageIndex = pageIndex
        #时间限制元组
        self.timeTuple = timeTuple
        #判断是否应该停止爬取mergeRequest列表
        self.shouldFinish = False


    #获取项目一页的MergeRequest的信息
    def getOnePageMergeRequestDataOfProject(self, projectId, mergeRequestIidList=[]):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
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
                if jsonList == None or len(jsonList) < self.numberOfMergeRequestInOnePage:
                    self.shouldFinish = True
                    print("获取mergeRequest列表完成，最后pageIndex为：" + str(self.pageIndex))
                idList = self.selectTimeSuitMergeRequest(jsonList)
                mergeRequestIidList.extend(idList)




    def getOnePageMergeRequestApi(self, repo_id):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_REQUESTS + \
              "?scope=all&state=all&page=" + str(self.pageIndex)
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
        # projectID = getParameterHelper.getProjectID()
        owner = utils.getOwnerFromUrl(url)
        repo = utils.getRepoFromUrl(url)
        projectID = utils.getProjectIdByOwnerAndRepo(owner, repo)
        # pages = getParameterHelper.getMergeRequestPages()
        pageIndex = 1
        mergeRequestIidList = []
        while True:
            helper = AsyncGetProjectInformationHelper(pageIndex, timeLimit)
            helper.getOnePageMergeRequestDataOfProject(projectID, mergeRequestIidList)
            if helper.shouldFinish:
                break
            pageIndex += 1
        return mergeRequestIidList

if __name__ == '__main__':
    arr = AsyncGetProjectInformationHelper.getMergeRequestIidList("https://gitlab.com/tezos/tezos", (2000, 9, 2020, 10))
    # for i in arr:
    #     print(i)
    # getParameterHelper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos")
    # projectID = getParameterHelper.getProjectID()
    # print(projectID)
    # pages = getParameterHelper.getMergeRequestPages()
    # for i in range(1, 3):
    #     helper = AsyncGetProjectInformationHelper(str(i))
    #     helper.getOnePageMergeRequestDataOfProject(projectID)

