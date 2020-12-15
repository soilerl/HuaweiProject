import aiohttp
import asyncio
import json

from datetime import datetime

import source.utils.ApiUtils as ApiUtils
import source.database.mongoDB.StringMongoDBUtils as StringMongoDBUtils

from source.utils.StringKeyUtils import StringKeyUtils
from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.config.configPraser import configPraser
from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.database.mongoDB.MongoUtil import MongoDBHelper


class AsyncGetProjectInformationHelper:

    pageIndex = 0

    #获取项目一页的MergeRequest的信息
    @staticmethod
    def getOnePageMergeRequestDataOfProject(projectId):
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(AsyncGetProjectInformationHelper.preProcess(projectId))]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

    @staticmethod
    async def preProcess(repo_id):
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        tasks = [asyncio.ensure_future(AsyncGetProjectInformationHelper.downloadInformation(repo_id, semaphore))]
        await asyncio.wait(tasks)

    #下载数据并写入数据库
    @staticmethod
    async def downloadInformation(repo_id, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = AsyncGetProjectInformationHelper.getProjectApi(repo_id)
                jsonList = await ApiUtils.fetchData(session, api)
                print(len(jsonList))
                dbHelper = MongoDBHelper()
                for mergeRequest in jsonList:
                    dbHelper.writeIntoDatabase(StringMongoDBUtils.COLLECTION_NAME_MERGEREQUEST, mergeRequest)


    @staticmethod
    def getProjectApi(repo_id):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_REQUESTS + \
              "?scope=all&state=all&page=" + str(AsyncGetProjectInformationHelper.pageIndex)
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, repo_id)
        return api

if __name__ == '__main__':
    getParameterHelper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos")
    projectID = getParameterHelper.getProjectID()
    pages = getParameterHelper.getMergeRequestPages()
    for i in range(1, 3):
        AsyncGetProjectInformationHelper.pageIndex = i
        AsyncGetProjectInformationHelper.getOnePageMergeRequestDataOfProject(projectID)
