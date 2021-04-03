import time
import json
from flask import Flask, request, logging
from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.data.service.AsyncProjectAllDataFetcher import AsyncProjectAllDataFetcher
from source.data.service.AsyncGetProjectMergeRequestInformationHelper import AsyncGetProjectInformationHelper
import source.utils.utils as utils
from analyzeData.runAllIndex import runAllIndex
from source.utils.pgsql import init as pgsql
from source.config.configPraser import configPraser
from source.utils.url import url as urls

#新引入
import schedule
from datetime import date,datetime,timezone




#更新某个项目的数据
def updateOneProjectData(url, date, projectId, createdAt):
    # url = "https://gitlab.com/tezos/tezos"
    # date = (2020, 9, 2020, 10)
    repo = utils.getRepoFromUrl(url)
    owner = utils.getOwnerFromUrl(url)
    mergeRequestIidList = AsyncGetProjectInformationHelper.getMergeRequestIidList(url, date)
    if mergeRequestIidList == None or len(mergeRequestIidList) == 0:
        return
    projectId = utils.getProjectIdByOwnerAndRepo(owner, repo)

    mergeRequestIidList.sort()
    limit = mergeRequestIidList[-1] - mergeRequestIidList[0]
    utils.mergeRequestFileExistAndDelete(repo)
    utils.notesFileExistAndDelete(repo)
    AsyncProjectAllDataFetcher.getDataForRepository(projectId, owner, repo, limit, mergeRequestIidList[-1])
    utils.indexFileExistAndDelete()
    metricDic = runAllIndex([repo], date)

    # data = json.dumps(metricDic)
    # pgsql.updateData(url, data)

    analyzeDataAndWriteToDatabase(projectId, url, createdAt, metricDic)

    return



#更新本地数据库中的数据
def updateData():
    createdAt = datetime.now(tz=timezone.utc)
    urlList = urls
    date = configPraser.getTimeRangeTuple()
    for projectId, url in urlList:
        updateOneProjectData(url, date, projectId, createdAt)


def analyzeDataAndWriteToDatabase(projectId, url, createdAt, metricDic={}):
    if metricDic == None or metricDic == {}:
        return

    commentDistributionByWeekdayList = metricDic["commentDistributionByWeekday"]
    projectName = utils.getRepoFromUrl(url)
    calTimeRange = str(configPraser.getTimeRangeTuple())
    metricName = "commentDistributionByWeekday"
    pgsql.writeWeekDayDataToDatabase(projectName, calTimeRange, createdAt, metricName, projectId, commentDistributionByWeekdayList[0])

    metricName = "commentDistributionByInterval"
    commentDistributionByIntervalList = metricDic["commentDistributionByInterval"]
    pgsql.writeDayPerHourDataToDatabase(projectName, calTimeRange, createdAt, metricName, projectId, commentDistributionByIntervalList[0])

    for metricName, metricDataList in metricDic.items():
        if metricName == "commentDistributionByWeekday" or metricName == "commentDistributionByInterval":
            continue
        for metricTime, metricData in metricDataList[0].items():
            pgsql.writeMonthDataToDatabase(projectName, calTimeRange, createdAt, metricName, projectId, metricTime, metricData)

if __name__ == '__main__':
    schedule.every().sunday.at(configPraser.getUpdateTime()).do(updateData)
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
        time.sleep(1)


