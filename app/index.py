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
def updateOneProjectData(url, date, projectId):
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

    analyzeDataAndWriteToDatabase(projectId, url, metricDic)

    return



#更新本地数据库中的数据
def updateData():
    urlList = urls
    date = configPraser.getTimeRangeTuple()
    for projectId, url in urlList:
        updateOneProjectData(url, date, projectId)


def analyzeDataAndWriteToDatabase(projectId, url, metricDic={}):
    if metricDic == None or metricDic == {}:
        return

    commentDistributionByWeekdayList = metricDic["commentDistributionByWeekday"]
    projectName = utils.getRepoFromUrl(url)
    calTimeRange = str(configPraser.getTimeRangeTuple())
    createdAt = datetime.now(tz=timezone.utc)
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
    schedule.every().day.at(configPraser.getUpdateTime()).do(updateData)
    while True:
        schedule.run_pending()  # 运行所有可运行的任务
        time.sleep(1)

    # dic = {"commentAcceptRatio": [{"2019-10": 0.41605839416058393, "2019-11": 0.6896551724137931, "2019-12": 0.6909090909090909, "2020-01": 0.26, "2020-02": 0.5221238938053098, "2020-03": 0.5537459283387622, "2020-04": 0.628, "2020-05": 0.5220588235294118, "2020-06": 0.44193548387096776, "2020-07": 0.4430379746835443, "2020-08": 0.3704918032786885, "2020-09": 0.5150684931506849, "2020-10": 0.4392156862745098}], "commentCount": [{"2019-10": 6.523809523809524, "2019-11": 3.8666666666666667, "2019-12": 5.238095238095238, "2020-01": 20.833333333333332, "2020-02": 5.136363636363637, "2020-03": 7.487804878048781, "2020-04": 8.333333333333334, "2020-05": 6.8, "2020-06": 7.560975609756097, "2020-07": 9.294117647058824, "2020-08": 12.708333333333334, "2020-09": 10.735294117647058, "2020-10": 6.375}], "commentDistributionByWeekday": [{"0": 569.0, "1": 531.0, "2": 445.0, "3": 489.0, "4": 398.0, "5": 10.0, "6": 39.0}], "commentDistributionByInterval": [{"0": 0.0, "1": 7.0, "2": 7.0, "3": 2.0, "4": 1.0, "5": 5.0, "6": 34.0, "7": 134.0, "8": 284.0, "9": 268.0, "10": 162.0, "11": 123.0, "12": 208.0, "13": 278.0, "14": 246.0, "15": 280.0, "16": 199.0, "17": 95.0, "18": 31.0, "19": 45.0, "20": 19.0, "21": 29.0, "22": 23.0, "23": 1.0}], "calReplyTime": [{"2019-10": 1146137.7160875634, "2019-11": 1583165.8481871344, "2019-12": 1327919.8975064976, "2020-01": 864394.3221199487, "2020-02": 1176098.0983225107, "2020-03": 1065942.161919053, "2020-04": 516089.10884923354, "2020-05": 374802.33212912484, "2020-06": 1067300.690398717, "2020-07": 698935.4837424761, "2020-08": 325208.9870872539, "2020-09": 535204.8735693828, "2020-10": 269651.91420253355}], "df_ended_time_avg": [{"2019-10": 78, "2019-11": 98, "2019-12": 119, "2020-01": 93, "2020-02": 19, "2020-03": 18, "2020-04": 37, "2020-05": 48, "2020-06": 10, "2020-07": 11, "2020-08": 142, "2020-09": 48, "2020-10": 10}], "df_opened_time_avg": [{"2019-10": 300, "2019-11": 62, "2019-12": 89, "2020-01": 220, "2020-02": 47, "2020-03": 32, "2020-04": 19, "2020-05": 98, "2020-06": 14, "2020-07": 18, "2020-08": 16, "2020-09": 98, "2020-10": 6}], "df_note_time_avg": [{"2019-10": 0, "2019-11": 79, "2019-12": 84, "2020-01": 1, "2020-02": 0, "2020-03": 5, "2020-04": 30, "2020-05": 6, "2020-06": 4, "2020-07": 1, "2020-08": 132, "2020-09": 0, "2020-10": 6}], "df_no_note_count": [{"2019-10": 312, "2019-11": 551, "2019-12": 863, "2020-01": 1157, "2020-02": 1517, "2020-03": 1601, "2020-04": 1653, "2020-05": 1285, "2020-06": 1233, "2020-07": 1331, "2020-08": 1284, "2020-09": 1319, "2020-10": 1402}], "df_has_note_count": [{"2019-10-01": 0, "2019-10-02": 0, "2019-10-03": 1, "2019-10-04": 1, "2019-10-05": 1, "2019-10-06": 1, "2019-10-07": 1, "2019-10-08": 1, "2019-10-09": 1, "2019-10-10": 1, "2019-10-11": 1, "2019-10-12": 1, "2019-10-13": 1, "2019-10-14": 2, "2019-10-15": 3, "2019-10-16": 2, "2019-10-17": 2, "2019-10-18": 2, "2019-10-19": 2, "2019-10-20": 2, "2019-10-21": 2, "2019-10-22": 2, "2019-10-23": 2, "2019-10-24": 2, "2019-10-25": 2, "2019-10-26": 2, "2019-10-27": 2, "2019-10-28": 6, "2019-10-29": 6, "2019-10-30": 4, "2019-10-31": 3, "2019-11-01": 3, "2019-11-02": 3, "2019-11-03": 3, "2019-11-04": 3, "2019-11-05": 4, "2019-11-06": 4, "2019-11-07": 6, "2019-11-08": 6, "2019-11-09": 6, "2019-11-10": 6, "2019-11-11": 6, "2019-11-12": 11, "2019-11-13": 11, "2019-11-14": 10, "2019-11-15": 9, "2019-11-16": 9, "2019-11-17": 9, "2019-11-18": 9, "2019-11-19": 10, "2019-11-20": 11, "2019-11-21": 10, "2019-11-22": 11, "2019-11-23": 11, "2019-11-24": 11, "2019-11-25": 11, "2019-11-26": 11, "2019-11-27": 11, "2019-11-28": 11, "2019-11-29": 9, "2019-11-30": 9, "2019-12-01": 9, "2019-12-02": 10, "2019-12-03": 10, "2019-12-04": 10, "2019-12-05": 10, "2019-12-06": 10, "2019-12-07": 10, "2019-12-08": 10, "2019-12-09": 9, "2019-12-10": 10, "2019-12-11": 13, "2019-12-12": 12, "2019-12-13": 12, "2019-12-14": 12, "2019-12-15": 12, "2019-12-16": 13, "2019-12-17": 14, "2019-12-18": 14, "2019-12-19": 14, "2019-12-20": 15, "2019-12-21": 15, "2019-12-22": 15, "2019-12-23": 15, "2019-12-24": 18, "2019-12-25": 18, "2019-12-26": 18, "2019-12-27": 18, "2019-12-28": 18, "2019-12-29": 18, "2019-12-30": 18, "2019-12-31": 18, "2020-01-01": 18, "2020-01-02": 16, "2020-01-03": 17, "2020-01-04": 17, "2020-01-05": 17, "2020-01-06": 18, "2020-01-07": 15, "2020-01-08": 17, "2020-01-09": 18, "2020-01-10": 19, "2020-01-11": 19, "2020-01-12": 18, "2020-01-13": 17, "2020-01-14": 16, "2020-01-15": 16, "2020-01-16": 15, "2020-01-17": 15, "2020-01-18": 15, "2020-01-19": 15, "2020-01-20": 16, "2020-01-21": 15, "2020-01-22": 14, "2020-01-23": 14, "2020-01-24": 15, "2020-01-25": 15, "2020-01-26": 15, "2020-01-27": 17, "2020-01-28": 15, "2020-01-29": 16, "2020-01-30": 16, "2020-01-31": 16, "2020-02-01": 16, "2020-02-02": 16, "2020-02-03": 17, "2020-02-04": 16, "2020-02-05": 16, "2020-02-06": 17, "2020-02-07": 18, "2020-02-08": 18, "2020-02-09": 18, "2020-02-10": 17, "2020-02-11": 15, "2020-02-12": 15, "2020-02-13": 14, "2020-02-14": 15, "2020-02-15": 14, "2020-02-16": 14, "2020-02-17": 18, "2020-02-18": 16, "2020-02-19": 16, "2020-02-20": 18, "2020-02-21": 19, "2020-02-22": 19, "2020-02-23": 19, "2020-02-24": 17, "2020-02-25": 15, "2020-02-26": 14, "2020-02-27": 15, "2020-02-28": 15, "2020-02-29": 15, "2020-03-01": 15, "2020-03-02": 17, "2020-03-03": 19, "2020-03-04": 21, "2020-03-05": 21, "2020-03-06": 22, "2020-03-07": 22, "2020-03-08": 22, "2020-03-09": 23, "2020-03-10": 21, "2020-03-11": 21, "2020-03-12": 23, "2020-03-13": 22, "2020-03-14": 22, "2020-03-15": 22, "2020-03-16": 22, "2020-03-17": 25, "2020-03-18": 23, "2020-03-19": 22, "2020-03-20": 21, "2020-03-21": 21, "2020-03-22": 21, "2020-03-23": 21, "2020-03-24": 20, "2020-03-25": 23, "2020-03-26": 24, "2020-03-27": 22, "2020-03-28": 22, "2020-03-29": 22, "2020-03-30": 25, "2020-03-31": 25, "2020-04-01": 27, "2020-04-02": 26, "2020-04-03": 27, "2020-04-04": 27, "2020-04-05": 27, "2020-04-06": 24, "2020-04-07": 26, "2020-04-08": 28, "2020-04-09": 28, "2020-04-10": 27, "2020-04-11": 27, "2020-04-12": 27, "2020-04-13": 27, "2020-04-14": 28, "2020-04-15": 27, "2020-04-16": 30, "2020-04-17": 28, "2020-04-18": 28, "2020-04-19": 28, "2020-04-20": 30, "2020-04-21": 27, "2020-04-22": 28, "2020-04-23": 27, "2020-04-24": 29, "2020-04-25": 29, "2020-04-26": 29, "2020-04-27": 29, "2020-04-28": 27, "2020-04-29": 29, "2020-04-30": 31, "2020-05-01": 31, "2020-05-02": 31, "2020-05-03": 31, "2020-05-04": 35, "2020-05-05": 32, "2020-05-06": 33, "2020-05-07": 34, "2020-05-08": 34, "2020-05-09": 34, "2020-05-10": 35, "2020-05-11": 32, "2020-05-12": 31, "2020-05-13": 34, "2020-05-14": 36, "2020-05-15": 35, "2020-05-16": 35, "2020-05-17": 35, "2020-05-18": 34, "2020-05-19": 35, "2020-05-20": 36, "2020-05-21": 36, "2020-05-22": 34, "2020-05-23": 33, "2020-05-24": 33, "2020-05-25": 35, "2020-05-26": 36, "2020-05-27": 38, "2020-05-28": 36, "2020-05-29": 34, "2020-05-30": 34, "2020-05-31": 34, "2020-06-01": 35, "2020-06-02": 39, "2020-06-03": 38, "2020-06-04": 38, "2020-06-05": 39, "2020-06-06": 39, "2020-06-07": 39, "2020-06-08": 38, "2020-06-09": 32, "2020-06-10": 33, "2020-06-11": 34, "2020-06-12": 34, "2020-06-13": 34, "2020-06-14": 34, "2020-06-15": 30, "2020-06-16": 33, "2020-06-17": 31, "2020-06-18": 31, "2020-06-19": 31, "2020-06-20": 31, "2020-06-21": 31, "2020-06-22": 30, "2020-06-23": 31, "2020-06-24": 32, "2020-06-25": 33, "2020-06-26": 33, "2020-06-27": 33, "2020-06-28": 33, "2020-06-29": 33, "2020-06-30": 32, "2020-07-01": 33, "2020-07-02": 31, "2020-07-03": 31, "2020-07-04": 31, "2020-07-05": 31, "2020-07-06": 32, "2020-07-07": 33, "2020-07-08": 32, "2020-07-09": 33, "2020-07-10": 35, "2020-07-11": 35, "2020-07-12": 35, "2020-07-13": 33, "2020-07-14": 33, "2020-07-15": 35, "2020-07-16": 33, "2020-07-17": 34, "2020-07-18": 34, "2020-07-19": 34, "2020-07-20": 31, "2020-07-21": 31, "2020-07-22": 33, "2020-07-23": 35, "2020-07-24": 37, "2020-07-25": 37, "2020-07-26": 37, "2020-07-27": 37, "2020-07-28": 37, "2020-07-29": 38, "2020-07-30": 38, "2020-07-31": 36, "2020-08-01": 36, "2020-08-02": 36, "2020-08-03": 37, "2020-08-04": 39, "2020-08-05": 40, "2020-08-06": 45, "2020-08-07": 46, "2020-08-08": 46, "2020-08-09": 47, "2020-08-10": 48, "2020-08-11": 48, "2020-08-12": 50, "2020-08-13": 50, "2020-08-14": 49, "2020-08-15": 49, "2020-08-16": 49, "2020-08-17": 45, "2020-08-18": 44, "2020-08-19": 44, "2020-08-20": 43, "2020-08-21": 43, "2020-08-22": 43, "2020-08-23": 43, "2020-08-24": 42, "2020-08-25": 41, "2020-08-26": 40, "2020-08-27": 40, "2020-08-28": 39, "2020-08-29": 38, "2020-08-30": 37, "2020-08-31": 39, "2020-09-01": 39, "2020-09-02": 38, "2020-09-03": 39, "2020-09-04": 39, "2020-09-05": 39, "2020-09-06": 40, "2020-09-07": 40, "2020-09-08": 37, "2020-09-09": 35, "2020-09-10": 33, "2020-09-11": 35, "2020-09-12": 35, "2020-09-13": 35, "2020-09-14": 33, "2020-09-15": 33, "2020-09-16": 32, "2020-09-17": 33, "2020-09-18": 33, "2020-09-19": 33, "2020-09-20": 33, "2020-09-21": 34, "2020-09-22": 30, "2020-09-23": 33, "2020-09-24": 34, "2020-09-25": 34, "2020-09-26": 34, "2020-09-27": 34, "2020-09-28": 37, "2020-09-29": 39, "2020-09-30": 39, "2020-10-01": 41, "2020-10-02": 42, "2020-10-03": 42, "2020-10-04": 42, "2020-10-05": 43, "2020-10-06": 44, "2020-10-07": 38, "2020-10-08": 37, "2020-10-09": 38, "2020-10-10": 38, "2020-10-11": 37, "2020-10-12": 41, "2020-10-13": 40, "2020-10-14": 39, "2020-10-15": 38, "2020-10-16": 39, "2020-10-17": 39, "2020-10-18": 39, "2020-10-19": 39, "2020-10-20": 38, "2020-10-21": 39, "2020-10-22": 39, "2020-10-23": 39, "2020-10-24": 39, "2020-10-25": 39, "2020-10-26": 37, "2020-10-27": 44, "2020-10-28": 44, "2020-10-29": 44, "2020-10-30": 42, "2020-10-31": 0}], "df_ended_count": [{"2019-10-01": 0, "2019-10-02": 1, "2019-10-03": 5, "2019-10-04": 7, "2019-10-05": 7, "2019-10-06": 8, "2019-10-07": 8, "2019-10-08": 10, "2019-10-09": 16, "2019-10-10": 16, "2019-10-11": 17, "2019-10-12": 17, "2019-10-13": 17, "2019-10-14": 18, "2019-10-15": 22, "2019-10-16": 23, "2019-10-17": 24, "2019-10-18": 25, "2019-10-19": 25, "2019-10-20": 25, "2019-10-21": 27, "2019-10-22": 27, "2019-10-23": 32, "2019-10-24": 33, "2019-10-25": 35, "2019-10-26": 35, "2019-10-27": 37, "2019-10-28": 40, "2019-10-29": 42, "2019-10-30": 50, "2019-10-31": 53, "2019-11-01": 54, "2019-11-02": 54, "2019-11-03": 54, "2019-11-04": 55, "2019-11-05": 55, "2019-11-06": 59, "2019-11-07": 60, "2019-11-08": 63, "2019-11-09": 63, "2019-11-10": 63, "2019-11-11": 63, "2019-11-12": 63, "2019-11-13": 66, "2019-11-14": 69, "2019-11-15": 75, "2019-11-16": 75, "2019-11-17": 75, "2019-11-18": 75, "2019-11-19": 76, "2019-11-20": 77, "2019-11-21": 80, "2019-11-22": 80, "2019-11-23": 80, "2019-11-24": 80, "2019-11-25": 81, "2019-11-26": 81, "2019-11-27": 82, "2019-11-28": 83, "2019-11-29": 87, "2019-11-30": 87, "2019-12-01": 87, "2019-12-02": 89, "2019-12-03": 93, "2019-12-04": 95, "2019-12-05": 95, "2019-12-06": 95, "2019-12-07": 95, "2019-12-08": 95, "2019-12-09": 100, "2019-12-10": 102, "2019-12-11": 107, "2019-12-12": 108, "2019-12-13": 108, "2019-12-14": 108, "2019-12-15": 108, "2019-12-16": 108, "2019-12-17": 109, "2019-12-18": 109, "2019-12-19": 113, "2019-12-20": 114, "2019-12-21": 114, "2019-12-22": 115, "2019-12-23": 115, "2019-12-24": 116, "2019-12-25": 116, "2019-12-26": 116, "2019-12-27": 116, "2019-12-28": 116, "2019-12-29": 116, "2019-12-30": 119, "2019-12-31": 119, "2020-01-01": 119, "2020-01-02": 121, "2020-01-03": 121, "2020-01-04": 121, "2020-01-05": 121, "2020-01-06": 122, "2020-01-07": 130, "2020-01-08": 132, "2020-01-09": 136, "2020-01-10": 136, "2020-01-11": 136, "2020-01-12": 138, "2020-01-13": 142, "2020-01-14": 145, "2020-01-15": 145, "2020-01-16": 147, "2020-01-17": 148, "2020-01-18": 148, "2020-01-19": 148, "2020-01-20": 149, "2020-01-21": 151, "2020-01-22": 157, "2020-01-23": 158, "2020-01-24": 158, "2020-01-25": 159, "2020-01-26": 159, "2020-01-27": 159, "2020-01-28": 164, "2020-01-29": 166, "2020-01-30": 167, "2020-01-31": 168, "2020-02-01": 168, "2020-02-02": 168, "2020-02-03": 168, "2020-02-04": 174, "2020-02-05": 177, "2020-02-06": 177, "2020-02-07": 179, "2020-02-08": 179, "2020-02-09": 179, "2020-02-10": 181, "2020-02-11": 187, "2020-02-12": 189, "2020-02-13": 191, "2020-02-14": 192, "2020-02-15": 193, "2020-02-16": 193, "2020-02-17": 196, "2020-02-18": 201, "2020-02-19": 203, "2020-02-20": 204, "2020-02-21": 204, "2020-02-22": 204, "2020-02-23": 204, "2020-02-24": 209, "2020-02-25": 215, "2020-02-26": 218, "2020-02-27": 219, "2020-02-28": 220, "2020-02-29": 220, "2020-03-01": 220, "2020-03-02": 221, "2020-03-03": 222, "2020-03-04": 223, "2020-03-05": 226, "2020-03-06": 226, "2020-03-07": 227, "2020-03-08": 233, "2020-03-09": 245, "2020-03-10": 251, "2020-03-11": 255, "2020-03-12": 256, "2020-03-13": 258, "2020-03-14": 258, "2020-03-15": 258, "2020-03-16": 261, "2020-03-17": 265, "2020-03-18": 268, "2020-03-19": 272, "2020-03-20": 277, "2020-03-21": 277, "2020-03-22": 278, "2020-03-23": 284, "2020-03-24": 292, "2020-03-25": 292, "2020-03-26": 299, "2020-03-27": 306, "2020-03-28": 306, "2020-03-29": 306, "2020-03-30": 309, "2020-03-31": 314, "2020-04-01": 318, "2020-04-02": 324, "2020-04-03": 325, "2020-04-04": 325, "2020-04-05": 325, "2020-04-06": 337, "2020-04-07": 342, "2020-04-08": 345, "2020-04-09": 346, "2020-04-10": 349, "2020-04-11": 349, "2020-04-12": 349, "2020-04-13": 349, "2020-04-14": 352, "2020-04-15": 353, "2020-04-16": 358, "2020-04-17": 362, "2020-04-18": 362, "2020-04-19": 362, "2020-04-20": 366, "2020-04-21": 371, "2020-04-22": 375, "2020-04-23": 378, "2020-04-24": 381, "2020-04-25": 381, "2020-04-26": 381, "2020-04-27": 383, "2020-04-28": 390, "2020-04-29": 394, "2020-04-30": 395, "2020-05-01": 395, "2020-05-02": 395, "2020-05-03": 395, "2020-05-04": 398, "2020-05-05": 404, "2020-05-06": 409, "2020-05-07": 417, "2020-05-08": 417, "2020-05-09": 417, "2020-05-10": 417, "2020-05-11": 428, "2020-05-12": 430, "2020-05-13": 432, "2020-05-14": 433, "2020-05-15": 434, "2020-05-16": 434, "2020-05-17": 434, "2020-05-18": 437, "2020-05-19": 441, "2020-05-20": 447, "2020-05-21": 447, "2020-05-22": 449, "2020-05-23": 450, "2020-05-24": 450, "2020-05-25": 451, "2020-05-26": 454, "2020-05-27": 454, "2020-05-28": 457, "2020-05-29": 460, "2020-05-30": 460, "2020-05-31": 460, "2020-06-01": 460, "2020-06-02": 462, "2020-06-03": 465, "2020-06-04": 469, "2020-06-05": 471, "2020-06-06": 471, "2020-06-07": 471, "2020-06-08": 480, "2020-06-09": 493, "2020-06-10": 498, "2020-06-11": 499, "2020-06-12": 505, "2020-06-13": 505, "2020-06-14": 505, "2020-06-15": 516, "2020-06-16": 519, "2020-06-17": 523, "2020-06-18": 524, "2020-06-19": 527, "2020-06-20": 527, "2020-06-21": 527, "2020-06-22": 537, "2020-06-23": 538, "2020-06-24": 540, "2020-06-25": 542, "2020-06-26": 543, "2020-06-27": 543, "2020-06-28": 543, "2020-06-29": 544, "2020-06-30": 546, "2020-07-01": 547, "2020-07-02": 553, "2020-07-03": 553, "2020-07-04": 553, "2020-07-05": 553, "2020-07-06": 556, "2020-07-07": 561, "2020-07-08": 563, "2020-07-09": 564, "2020-07-10": 565, "2020-07-11": 565, "2020-07-12": 565, "2020-07-13": 572, "2020-07-14": 572, "2020-07-15": 574, "2020-07-16": 579, "2020-07-17": 584, "2020-07-18": 584, "2020-07-19": 584, "2020-07-20": 590, "2020-07-21": 591, "2020-07-22": 593, "2020-07-23": 594, "2020-07-24": 594, "2020-07-25": 594, "2020-07-26": 594, "2020-07-27": 601, "2020-07-28": 604, "2020-07-29": 604, "2020-07-30": 604, "2020-07-31": 608, "2020-08-01": 608, "2020-08-02": 608, "2020-08-03": 609, "2020-08-04": 609, "2020-08-05": 611, "2020-08-06": 611, "2020-08-07": 612, "2020-08-08": 612, "2020-08-09": 612, "2020-08-10": 613, "2020-08-11": 615, "2020-08-12": 617, "2020-08-13": 620, "2020-08-14": 622, "2020-08-15": 622, "2020-08-16": 622, "2020-08-17": 627, "2020-08-18": 629, "2020-08-19": 630, "2020-08-20": 633, "2020-08-21": 634, "2020-08-22": 634, "2020-08-23": 634, "2020-08-24": 637, "2020-08-25": 640, "2020-08-26": 641, "2020-08-27": 643, "2020-08-28": 646, "2020-08-29": 647, "2020-08-30": 648, "2020-08-31": 648, "2020-09-01": 651, "2020-09-02": 655, "2020-09-03": 661, "2020-09-04": 666, "2020-09-05": 666, "2020-09-06": 667, "2020-09-07": 673, "2020-09-08": 682, "2020-09-09": 687, "2020-09-10": 689, "2020-09-11": 691, "2020-09-12": 691, "2020-09-13": 691, "2020-09-14": 695, "2020-09-15": 695, "2020-09-16": 697, "2020-09-17": 697, "2020-09-18": 697, "2020-09-19": 697, "2020-09-20": 697, "2020-09-21": 698, "2020-09-22": 702, "2020-09-23": 704, "2020-09-24": 706, "2020-09-25": 706, "2020-09-26": 706, "2020-09-27": 707, "2020-09-28": 708, "2020-09-29": 709, "2020-09-30": 712, "2020-10-01": 713, "2020-10-02": 715, "2020-10-03": 715, "2020-10-04": 715, "2020-10-05": 717, "2020-10-06": 725, "2020-10-07": 737, "2020-10-08": 741, "2020-10-09": 743, "2020-10-10": 743, "2020-10-11": 744, "2020-10-12": 746, "2020-10-13": 749, "2020-10-14": 752, "2020-10-15": 756, "2020-10-16": 756, "2020-10-17": 756, "2020-10-18": 757, "2020-10-19": 759, "2020-10-20": 762, "2020-10-21": 764, "2020-10-22": 771, "2020-10-23": 774, "2020-10-24": 776, "2020-10-25": 776, "2020-10-26": 781, "2020-10-27": 782, "2020-10-28": 785, "2020-10-29": 785, "2020-10-30": 789, "2020-10-31": 0}], "mrClosedRatio": [{"2019-10": 0.2602739726027397, "2019-11": 0.2857142857142857, "2019-12": 0.1956521739130435, "2020-01": 0.22950819672131148, "2020-02": 0.2545454545454545, "2020-03": 0.17272727272727273, "2020-04": 0.29069767441860467, "2020-05": 0.1320754716981132, "2020-06": 0.14285714285714285, "2020-07": 0.13636363636363635, "2020-08": 0.125, "2020-09": 0.19117647058823528, "2020-10": 0.14666666666666667}], "mrOpenedRatio": [{"2019-10": 0.0, "2019-11": 0.0, "2019-12": 0.0, "2020-01": 0.04918032786885246, "2020-02": 0.01818181818181818, "2020-03": 0.02727272727272727, "2020-04": 0.011627906976744186, "2020-05": 0.018867924528301886, "2020-06": 0.07692307692307693, "2020-07": 0.015151515151515152, "2020-08": 0.1, "2020-09": 0.04411764705882353, "2020-10": 0.06666666666666667}], "mrMergedRatio": [{"2019-10": 0.7397260273972602, "2019-11": 0.7142857142857143, "2019-12": 0.8043478260869565, "2020-01": 0.7213114754098361, "2020-02": 0.7272727272727273, "2020-03": 0.8, "2020-04": 0.6976744186046512, "2020-05": 0.8490566037735849, "2020-06": 0.7802197802197802, "2020-07": 0.8484848484848485, "2020-08": 0.775, "2020-09": 0.7647058823529411, "2020-10": 0.7866666666666666}]}
    # analyzeDataAndWriteToDatabase(3836952, "https://gitlab.com/tezos/tezos", dic)


