import pymongo
import datetime
import re
import xlrd as xlrd
import analyzeData.common as common

import analyzeData.common as common
from pandas import DataFrame
from source.utils.ExcelHelper import ExcelHelper
"""计算问题单数量"""

def connectMongoDB(collectionName=''):
    client = pymongo.MongoClient(host='10.244.201.143', port=8635)
    db = client["wisedevops"]
    db.authenticate("dataoffice", "Huawei_123")
    collection = db[collectionName]
    return collection

#分析数据，传入服务名和限制时间,返回所有符合条件的问题单数据
def analyzeData(serviceName='', date=()) -> []:
    res = []
    dTSVoCollection = connectMongoDB("dTSVo")
    serviceName = serviceName.strip()
    dtsDict = dTSVoCollection.find({"sbaseline" : re.compile(serviceName.strip())})

    yearMin = date[0]
    monthMin = date[1]
    yearMax = date[2]
    monthMax = date[3]

    for dts in dtsDict:
        createdAt = dts["dtimecreated"]
        createdAtYear = createdAt.year
        createdAtMonth = createdAt.month
        if  createdAtYear >= yearMin and createdAtYear <= yearMax:
            if createdAtMonth >= monthMin and createdAtMonth <= monthMax:
                res.append(dts)

    return res

#构建空的dateFrame
def createDf(date=()) -> DataFrame:
    columns = ["project"]
    columns.extend(common.getTimeLableFromTime(common.getTimeListFromTuple(date)))
    dtsNumberDf = DataFrame(columns=columns)
    return dtsNumberDf

def calDtsNumberDic(projectName, date=()):
    resDict = {}
    dtsList = analyzeData(projectName, date)
    for dts in dtsList:
        createdAt = dts["dtimecreated"]
        month = createdAt.month
        year = createdAt.year
        if month < 10:
            monthStr = str(0) + str(month)
        else:
            monthStr = str(month)
        key = str(year) + str("-") + monthStr
        if key in resDict.keys():
            resDict[key] += 1
        else:
            resDict[key] = 1
    resDict["project"] = projectName
    return resDict

#计算问题单的数量
def calDtsNumber(serviceName='', date=(), dtsNumberDf=DataFrame):
    dtsDic = calDtsNumberDic(serviceName, date)
    dtsNumberDf = dtsNumberDf.append(dtsDic, ignore_index=True)
    return dtsNumberDf

#计算问题反馈率（问题单数/mr数）
def calDtsRate(projectName='', date=(), df=DataFrame):
    dtsDic = calDtsNumberDic(projectName, date=date)
    mrDic = getMrCountDic(projectName, date)
    resDic = {}
    for k, v in dtsDic.items():
        if k == 'project':
            continue
        mrCount = 1
        if k in mrDic.keys():
            mrCount = mrDic[k]
        temp = int(dtsDic[k]) / int(mrCount)
        resDic[k] = temp
    resDic["project"] = projectName
    df = df.append(resDic, ignore_index=True)
    return df

#计算mr数量
def getMrCountDic(projectName='', date=()):
    mrList = common.getMergeRequestInstances(projectName)
    resDict = {}
    for mr in mrList:
        createdAt = mr.created_at
        time = common.tranformStrToDateTime(createdAt)
        if common.checkTime(time, date):
            monthStr = ''
            if time.month < 10:
                monthStr = '0' + str(time.month)
            else:
                monthStr = str(time.month)
            timeStr = str(time.year) + "-" + monthStr
            if timeStr in resDict.keys():
                resDict[timeStr] += 1
            else:
                resDict[timeStr] = 1
    resDict["project"] = projectName
    return resDict

def getServiceNameList(excelName, sheetName):
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_name(sheetName)
    rows = sheet.nrows
    serviceNameList = sheet.col_values(0, 1)
    dic = {}
    for serviceName in serviceNameList:
        dic[serviceName] = 1
    return list(dic.keys())

def getSpnameNameList(excelName, sheetName):
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_name(sheetName)
    rows = sheet.nrows
    serviceNameList = sheet.col_values(2, 1)
    dic = {}
    for serviceName in serviceNameList:
        dic[serviceName] = 1
    return list(dic.keys())

#计算一个项目的所有问题单之和
def calAllDtsOfProject(serviceNameList, date=()):
    dtsNumberDicList = []
    for serviceName in serviceNameList:
        print(serviceName)
        dtsNumberDic = calDtsNumberDic(serviceName, date)
        dtsNumberDicList.append(dtsNumberDic)
    sumDic = {}
    for dtsDic in dtsNumberDicList:
        for k, v in dtsDic.items():
            if k == 'project':
                continue
            if k in sumDic:
                sumDic[k] += v
            else:
                sumDic[k] = v
    return sumDic
#计算一个项目的所有mr和
def calAllMrsOfProject(serviceNameList, date=()):
    mrDicList = []
    for serviceName in serviceNameList:
        print(serviceName)
        mrDic = getMrCountDic(serviceName, date)
        mrDicList.append(mrDic)
    sumDic = {}
    for mrDic in mrDicList:
        for k, v in mrDic.items():
            if k == 'project':
                continue
            if k in sumDic:
                sumDic[k] += v
            else:
                sumDic[k] = v
    return sumDic

if __name__ == '__main__':
    #云平台
    serviceNameList = ["WiseCloudIMService", "WiseCloudHOTAService", "WiseCloudMediaHostingService",
                       "WiseCloudSNService", "WiseCloudContentCommunityService"]

    #pps
    # serviceNameList = getServiceNameList('PPS9个服务去重整理.xlsx', 'de_duplicates')
    # spnameList = getSpnameNameList('PPS9个服务去重整理.xlsx', 'de_duplicates')

    # fileName = "dtsNumber.xls"
    # sheetName = "dtsNumber"
    # df = createDf((2019, 9, 2020, 11))
    # for serviceName in serviceNameList:
    #     df = calDtsNumber(serviceName, (2019, 9, 2020, 11), df)
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    # print(df)

    fileName = "dtsRate.xls"
    sheetName = "dtsRate"
    df = createDf((2019, 9, 2020, 11))
    #PPS
    # dtsSumDic = calAllDtsOfProject(serviceNameList, (2019, 9, 2020, 11))
    # mrSumDic = calAllMrsOfProject(spnameList, (2019, 9, 2020, 11))
    #云平台
    dtsSumDic = calAllDtsOfProject(serviceNameList, (2019, 9, 2020, 11))
    mrSumDic = calAllMrsOfProject(serviceNameList, (2019, 9, 2020, 11))
    resDic = {}
    for k in dtsSumDic.keys():
        if k == 'project':
            continue
        mrCount = 1
        if k in mrSumDic.keys():
            mrCount = mrSumDic[k]
        temp = int(dtsSumDic[k]) / int(mrCount)
        resDic[k] = temp
    resDic["project"] = "wiseContent"
    df = df.append(resDic, ignore_index=True)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print(df)



