import asyncio
import aiohttp
import warnings
import source.utils.utils as utils
from source.utils.StringKeyUtils import StringKeyUtils
from source.data.service.AsyncApiHelper import AsyncApiHelper


class AsyncGetDataFromGitlabHelper:

    def __init__(self, api=''):
        self.api = api
        #最终获取的数据存储在res里
        self.res = None

    #对外暴露的接口
    def downLoadInformationByApi(self):
        # new_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(self.__preProcess())]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

    async def __preProcess(self):
        semaphore = asyncio.Semaphore(20)
        tasks = [asyncio.ensure_future(self.__downloadInformation(semaphore))]
        await asyncio.wait(tasks)


    #将下载好的数据赋值给实例的jsonList属性
    async def __downloadInformation(self, semaphore):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                res = await self.__fetchData(session)
                self.res = res

    # 异步获取数据，传入aiohttp.ClientSession和api
    async def __fetchData(self, session):
        headers = utils.getHeader()
        try:
            async with session.get(self.api, ssl=False, headers=headers, timeout=60) as response:
                print("response status: ", response.status)
                if response.status == 403:
                    raise 403
                return await response.json()
        except Exception as e:
            print(e)
            return await self.__fetchData(session, self.api)

if __name__ == '__main__':
    url = "https://gitlab.com/tezos/tezos"
    repo = utils.getRepoFromUrl(url)
    owner = utils.getOwnerFromUrl(url)
    projectId = utils.getProjectIdByOwnerAndRepo(owner, repo)
    api = StringKeyUtils.API_GITLAB + "/projects/" + projectId
    helper = AsyncGetDataFromGitlabHelper(api)
    helper.downLoadInformationByApi()
    res = helper.res
    if res is not None:
        print(res)
        print(len(res))

