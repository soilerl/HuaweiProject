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

    # 存放符合要求的mergeRequest的iid
    mergeRequestIdList = []

    def __init__(self, pageIndex='', timeTuple=()):
        self.pageIndex =pageIndex
        #时间限制元组
        self.timeTuple = timeTuple



    #获取项目一页的MergeRequest的信息
    def getOnePageMergeRequestDataOfProject(self, projectId):
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(self.preProcess(projectId))]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

    async def preProcess(self, repo_id):
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        tasks = [asyncio.ensure_future(self.downloadInformation(repo_id, semaphore))]
        await asyncio.wait(tasks)

    #下载数据并写入数据库
    async def downloadInformation(self, repo_id, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = self.getOnePageMergeRequestApi(repo_id)
                jsonList = await ApiUtils.fetchData(session, api)
                print(jsonList)

    def getOnePageMergeRequestApi(self, repo_id):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_REQUESTS + \
              "?scope=all&state=all&page=" + self.pageIndex + ""
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, repo_id)
        return api

    # def selectTimeSuitMergeRequest(self, mergeRequestList=[]):


if __name__ == '__main__':
    getParameterHelper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos", (2019, 9, 2020, 10))
    projectID = getParameterHelper.getProjectID()
    pages = getParameterHelper.getMergeRequestPages()
    for i in range(1, 3):
        helper = AsyncGetProjectInformationHelper(str(i))
        helper.getOnePageMergeRequestDataOfProject(projectID)
