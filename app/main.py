from flask import Flask

from source.data.service.GetInformationOfParameter import GetInformationOfParameterHelper
from source.data.service.AsyncProjectAllDataFetcher import AsyncProjectAllDataFetcher
from source.data.service.AsyncGetProjectMergeRequestInformationHelper import AsyncGetProjectInformationHelper

app = Flask(__name__)

@app.route('/getData')
def getData():
    mergeRequestIidList = AsyncGetProjectInformationHelper.getMergeRequestIidList("https://gitlab.com/tezos/tezos",
                                                                                  (2020, 9, 2020, 10))
    url = ''
    helper = GetInformationOfParameterHelper(url)
    projectId = helper.getProjectID(url)
    owner = ''
    repo = ''
    mergeRequestIidList.sort()
    limit = mergeRequestIidList[-1] - mergeRequestIidList[0]
    AsyncProjectAllDataFetcher.getDataForRepository(projectId, owner, repo, limit, mergeRequestIidList[-1])

