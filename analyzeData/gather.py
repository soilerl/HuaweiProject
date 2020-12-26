from analyzeData.calReplyTime import classifyByTimeByProject
from analyzeData.commentAcceptRate import commentAcceptRate
from analyzeData.commentDistribution import commentDistribution

from source.utils.ExcelHelper import ExcelHelper
import pandas
import pandas as pd
import datetime
import xlrd as xlrd
#运行所有指标
def runAllIndex(projectNameList=[], date=()) -> bool:
    fileName = "project_index.xls"

    df = commentAcceptRate.commentAcceptRatioByProject(projectNameList, date)
    sheetName = "commentAcceptRatio"
    ExcelHelper.writeDataFrameToExcel(fileName, sheetName, df)
    print("commentAcceptRatio calculate finished！")

    df = commentDistribution.commentDistributionByProject(projectNameList, date)
    sheetName = "commentDistributionAll"
    ExcelHelper.writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionALL calculate finished！")

    df = commentDistribution.commentDistributionByProjectWithWeekDay(projectNameList, date, df)
    sheetName = "commentDistributionByWeekday"
    ExcelHelper.writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByWeekday calculate finished！")

    # 时间的单独统计
    df = commentDistribution.commentDistributionByProjectWithInterval(projectNameList, date, df)
    sheetName = "commentDistributionByInterval"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByInterval calculate finished！")

    df = classifyByTimeByProject(projectNameList, date)
    sheetName = "calReplyTime"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("calReplyTime calculate finished！")
    return True
    # try:
    #
    # except Exception as e:
    #     print(e)
    #     return False

if __name__ == '__main__':
    runAllIndex("tezos", ((2019, 9, 2020, 11)))