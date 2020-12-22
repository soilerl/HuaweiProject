from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.config.configPraser import configPraser


#异步获取数据，传入aiohttp.ClientSession和api
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
        return await fetchData(session, api)