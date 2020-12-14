import aiohttp
import asyncio
import json

from datetime import datetime

from source.utils.StringKeyUtils import StringKeyUtils
from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.config.configPraser import configPraser


class AsyncGetProjectInformationHelper:
    """获取项目的所有信息"""

    @staticmethod
    def getDataOfProject(repo_id):
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(AsyncGetProjectInformationHelper.preProcess(repo_id))]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

    @staticmethod
    async def preProcess(repo_id):
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        tasks = [asyncio.ensure_future(AsyncGetProjectInformationHelper.downloadInformation(repo_id, semaphore))]
        await asyncio.wait(tasks)


    @staticmethod
    async def downloadInformation(repo_id, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                api = AsyncGetProjectInformationHelper.getProjectApi(repo_id)
                jsonList = await AsyncGetProjectInformationHelper.fetchData(session, api)
                print(len(jsonList))
                for v in jsonList:
                    print(v)

    @staticmethod
    async def fetchData(session, api):
        headers = {}
        headers = AsyncApiHelper.getUserAgentHeaders(headers)
        headers = AsyncApiHelper.getPrivateTokensHeaders(headers)
        proxy = await AsyncApiHelper.getProxy()
        try:
            async with session.get(api, ssl=False, proxy=proxy
                    , headers=headers, timeout=configPraser.getTimeout()) as response:
                print("response status: ", response.status)
                if response.status == 403:
                    raise 403
                return await response.json()
        except Exception as e:
            print(e)
            return await AsyncGetProjectInformationHelper.fetchData(session, api)

    @staticmethod
    def getProjectApi(repo_id):
        api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_GITLAB_MERGE_REQUESTS + "?scope=all&state=all&page=1"
        api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, repo_id)
        return api

if __name__ == '__main__':
    AsyncGetProjectInformationHelper.getDataOfProject('3836952')