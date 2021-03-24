import time
from flask import Flask, request, logging

from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.data.service.AsyncProjectAllDataFetcher import AsyncProjectAllDataFetcher
from source.data.service.AsyncGetProjectMergeRequestInformationHelper import AsyncGetProjectInformationHelper
import source.utils.utils as utils
from analyzeData.runAllIndex import runAllIndex

app = Flask(__name__)

@app.route("/test", methods=['GET'])
def test():
    time.sleep(300)
    return 'helloworld'

#更新数据
@app.route('/updateData', methods=['GET'])
def updateData():
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
    return

#获取数据
@app.route('/getData', methods=['GET'])
def getData():
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


