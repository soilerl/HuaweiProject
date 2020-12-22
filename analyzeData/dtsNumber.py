import pymongo
import datetime
import analyzeData.common as common
from pandas import DataFrame
from source.utils.ExcelHelper import ExcelHelper
"""计算问题单数量"""

def connectMongoDB():
    client = pymongo.MongoClient(host='10.244.201.143', port=8635)
    db = client["wisedevops"]
    db.authenticate("dataoffice", "Huawei_123")
    collection = db["dTSVo"]
    return collection

#分析数据，传入服务名和起始时间,返回所有符合条件的问题单数据
def analyzeData(serviceName='', timeIndexStr='') -> []:
    res = []
    dTSVoCollection = connectMongoDB()
    dtsDict = dTSVoCollection.find({"sServiceName" : serviceName})
    timeIndex = datetime.datetime.strptime(timeIndexStr,'%Y-%m-%d %H:%M:%S')
    timeIndexStamp = timeIndex.timestamp()
    for dts in dtsDict:
        createdAt = dts["dtimecreated"]
        createdATStamp = createdAt.timestamp()
        timeDiff = createdATStamp - timeIndexStamp
        if timeDiff < 0:
            continue
        res.append(dts)
    return res

def calDtsNumber(serviceName='', timeIndexStr='', date=()):
    resDict = {}
    dtsList = analyzeData(serviceName, timeIndexStr)
    columns = ["project"]
    columns.extend(common.getTimeLableFromTime(common.getTimeListFromTuple(date)))
    dtsNumberDf = DataFrame(columns=columns)
    dtsNumberDf = DataFrame(columns=columns)
    for dts in dtsList:
        createdAt = dts["dtimecreated"]
        month = createdAt.month
        year = createdAt.year
        if month < 10:
            monthStr = str(0) + str(month)
        key = str(year) + str("-") + monthStr
        if key in resDict.keys():
            resDict[key] += 1
        else:
            resDict[key] = 1
    resDict["project"] = serviceName
    dtsNumberDf = dtsNumberDf.append(resDict, ignore_index=True)
    return dtsNumberDf

if __name__ == '__main__':
    df = calDtsNumber("WiseCloudIMService", "2019-09-01 00:00:00", (2019, 9, 2020, 11))
    fileName = "dtsNumber.xls"
    sheetName = "dtsNumber"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)