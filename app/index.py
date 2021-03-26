import time
import json
from flask import Flask, request, logging
from apscheduler.schedulers.blocking import BlockingScheduler
from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.data.service.AsyncProjectAllDataFetcher import AsyncProjectAllDataFetcher
from source.data.service.AsyncGetProjectMergeRequestInformationHelper import AsyncGetProjectInformationHelper
import source.utils.utils as utils
from analyzeData.runAllIndex import runAllIndex
from source.utils.pgsql import init as pgsql
from source.config.configPraser import configPraser

#新引入
import schedule




# @app.route("/test", methods=['GET'])
def test():
    time.sleep(300)
    return 'helloworld'

#更新某个项目的数据
def updateOneProjectData(url, date=()):
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
    indexDic = runAllIndex([repo], date)
    data = json.dumps(indexDic)
    pgsql.updateData(url, data)
    return

#获取数据
# @app.route('/getData', methods=['GET'])
def getData():
    try:
        url = request.args['url']
        dateStr = request.args['date']
        dateArr = dateStr.split(',')
        date = (int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(dateArr[3]))
        # url = "https://gitlab.com/tezos/tezos"
        # date = (2020, 9, 2020, 10)
        repo = utils.getRepoFromUrl(url)
        owner = utils.getOwnerFromUrl(url)
        mergeRequestIidList = AsyncGetProjectInformationHelper.getMergeRequestIidList(url, date)

        projectId = utils.getProjectIdByOwnerAndRepo(owner, repo)

        mergeRequestIidList.sort()
        limit = mergeRequestIidList[-1] - mergeRequestIidList[0]
        utils.mergeRequestFileExistAndDelete(repo)
        utils.notesFileExistAndDelete(repo)
        AsyncProjectAllDataFetcher.getDataForRepository(projectId, owner, repo, limit, mergeRequestIidList[-1])
        utils.indexFileExistAndDelete()
        indexDic = runAllIndex([repo], date)
        return indexDic
    except:
        print(url)
        print(mergeRequestIidList)


#更新本地数据库中的数据
def updateData():
    urlsStr = configPraser.getAllUrl()
    urlList = urlsStr.split(',')
    date = configPraser.getTimeRangeTuple()
    for url in urlList:
        updateOneProjectData(url, date)



if __name__ == '__main__':
    schedule.every().day.at("20:11").do(updateData)
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
        time.sleep(1)



    # updateData()