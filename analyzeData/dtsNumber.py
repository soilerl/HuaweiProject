import pymongo
import datetime
import re
import xlrd as xlrd


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
    dtsDict = dTSVoCollection.find({"sbaseline" : re.compile(serviceName)})

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

def calDtsNumber(serviceName='', date=(), dtsNumberDf=DataFrame):
    resDict = {}
    dtsList = analyzeData(serviceName, date)
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
    resDict["project"] = serviceName
    dtsNumberDf = dtsNumberDf.append(resDict, ignore_index=True)
    return dtsNumberDf

def getServiceNameList(excelName, sheetName):
    excel = xlrd.open_workbook(excelName)
    sheet = excel.sheet_by_name(sheetName)
    serviceNameList = sheet.col_values(0)[1:]
    dic  = {}
    for serviceName in serviceNameList:
        dic[serviceName] = 1
    return list(dic.keys())


if __name__ == '__main__':

    # serviceNameList = ["WiseCloudIMService", "WiseCloudHOTAService", "WiseCloudMediaHostingService",
    #                    "WiseCloudSNService", "WiseCloudContentCommunityService"]


    serviceNameList = getServiceNameList('PPS9个服务去重整理.xlsx', 'de_duplicates')
    fileName = "dtsNumber.xls"
    sheetName = "dtsNumber"
    df = createDf((2019, 9, 2020, 11))
    for serviceName in serviceNameList:
        df = calDtsNumber(serviceName, (2019, 9, 2020, 11), df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print(df)



