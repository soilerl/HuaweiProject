import source.utils.utils as utils
import analyzeData.common as common
from source.utils.StringKeyUtils import StringKeyUtils
from source.utils.asyncGetDataFromGitlabHelper import AsyncGetDataFromGitlabHelper
from pandas import DataFrame
from source.utils.ExcelHelper import ExcelHelper

#获取某个仓库的所有issue
def getIssuesOfProject(owner='', repoName='', pageIndex=''):
    # projectId = utils.getProjectIdByOwnerAndRepo(owner, repoName)
    projectId = str(8817162)
    api = StringKeyUtils.API_GITLAB + StringKeyUtils.API_ISSUE_OF_PROJECT + "?page=" + pageIndex
    api = api.replace(StringKeyUtils.STR_GITLAB_REPO_ID, projectId)
    helper = AsyncGetDataFromGitlabHelper(api)
    helper.downLoadInformationByApi()
    if helper.res == None:
        print("爬取issue失败")
    return helper.res

#构建空的dateFrame
def createDf(date=()) -> DataFrame:
    columns = ["project"]
    columns.extend(common.getTimeLableFromTime(common.getTimeListFromTuple(date)))
    dtsNumberDf = DataFrame(columns=columns)
    return dtsNumberDf

if __name__ == '__main__':
    res = []
    pageIndex = 1
    while True:
        temp = getIssuesOfProject("adblockplus", "libadblockplus-android", str(pageIndex))
        res.extend(temp)
        if temp == None or len(temp) < 20:
            break
        pageIndex += 1
    date = (2019, 9,  2020, 11)
    df = createDf(date)
    resDict = {}
    for r in res:
        created_at = r['created_at']
        time = common.tranformStrToDateTime(created_at)
        if common.checkTime(time, date):
            if time.month < 10:
                monthStr = '0' +  str(time.month)
            timeStr = str(time.year) + "-" + monthStr
            if timeStr in resDict.keys():
                resDict[timeStr] += 1
            else:
                resDict[timeStr] = 1
    resDict["project"] = "libadblockplus-android"
    df = df.append(resDict, ignore_index=True)
    print(df)
    fileName = "project_index.xls"
    sheetName = "dtsNumber"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)