import asyncio
import aiohttp

import source.utils.ApiUtils as ApiUtils
import source.database.mongoDB.StringMongoDBUtils as StringMongoDBUtils

from source.config.configPraser import configPraser
from source.utils.StringKeyUtils import StringKeyUtils
from source.database.mongoDB.MongoUtil import singleton


class AsyncGetNotesHelper:
    mergeRequestIid = ''
    projectId = ''

    def __init__(self, projectId, mergeRequestIid):
        self.projectId = projectId
        self.mergeRequestIid = mergeRequestIid


    # 获取某个mergeRequest
    def getNotesOfMergeRequest(self):
        if self.mergeRequestIid == '' or self.projectId == '':
            raise Exception("mergeRequestIid或projectId未赋值")
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(self.preProcess())]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)


    async def preProcess(self):
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        tasks = [asyncio.ensure_future(self.downloadInformation(semaphore))]
        await asyncio.wait(tasks)


    async def downloadInformation(self, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = self.getNotesOfMergeRequestApi()
                notesDictList = await ApiUtils.fetchData(session, api)
                for note in notesDictList:
                    #由于note中缺少projectId和mergeRequestIid，因此补上
                    note["projectId"] = self.projectId
                    note["mergeRequestIid"] = self.mergeRequestIid




    def getNotesOfMergeRequestApi(self):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_NOTES
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, self.projectId)
        api = api.replace(StringKeyUtils.STR_GITLAB_MR_NUMBER, self.mergeRequestIid)
        return api

if __name__ == '__main__':
    getNotesHelper = AsyncGetNotesHelper(str(3836952), str(2388))
    getNotesHelper.getNotesOfMergeRequest()