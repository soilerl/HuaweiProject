from analyzeData.calReplyTime import classifyByTimeByProject
from analyzeData.commentAcceptRate import commentAcceptRate
from analyzeData.commentDistribution import commentDistribution
from analyzeData.mrRate import MergeRequestRate
from analyzeData.timeAvg import TimeAvg
from analyzeData.timeSpan import TimeSpan
from analyzeData.commentCount import commentCount
from source.utils.ExcelHelper import ExcelHelper
import analyzeData.common as common
import pandas
import pandas as pd
import datetime
import xlrd as xlrd
from source.utils.StringKeyUtils import StringKeyUtils as sku




# def getDataFromExcel():
#     excel = xlrd.open_workbook(r'PPS9个服务去重整理.xlsx')
#     sheet = excel.sheet_by_name('de_duplicates')
#     spnameList = sheet.col_values(2)[1:]
#     dic = {}
#     for spname in spnameList:
#         dic[spname] = 1
#     return list(dic.keys())





    #跑所有指标
def runAllIndex(cProject_list=[], DATE=()) -> {}:
    resDic = {}
    cProject_list = cProject_list
    DATE = DATE
    timeList = common.getTimeListFromTuple(DATE)
    timeLabel = common.getTimeLableFromTime(timeList)
    df = commentAcceptRate.commentAcceptRatioByProject(cProject_list, DATE)
    resDic["commentAcceptRatio"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentAcceptRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentAcceptRatio calculate finished！")

    df = commentCount.commentCountByProject(cProject_list, DATE)
    resDic["commentCount"] = common.transformDfIntoArr(df)

    baseDf = commentDistribution.commentDistributionByProject(cProject_list, DATE)
    # resDic["commentDistributionALL"] = common.transformDfIntoArr(baseDf, DATE)
    # """时间和周的交叉详细统计，描述看文档"""
    # """计算的df写入xlsx"""
    # fileName = "project_index.xls"
    # sheetName = "commentDistributionALL"
    # # print(df)
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, baseDf)
    # print("commentDistributionALL calculate finished！")

    df = commentDistribution.commentDistributionByProjectWithWeekDay(cProject_list, DATE, baseDf)
    resDic["commentDistributionByWeekday"] = common.transformDfIntoArr(df)
    """周的单独统计，描述看文档"""
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentDistributionByWeekday"
    # print(df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByWeekday calculate finished！")

    df = commentDistribution.commentDistributionByProjectWithInterval(cProject_list, DATE, baseDf)
    resDic["commentDistributionByInterval"] = common.transformDfIntoArr(df)
    """时间的单独统计，描述看文档"""
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentDistributionByInterval"
    # print(df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByInterval calculate finished！")

    df = classifyByTimeByProject(cProject_list, DATE)
    resDic["calReplyTime"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "calReplyTime"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("calReplyTime calculate finished！")

    # time avg
    ta = TimeAvg(cProject_list, DATE)
    df1 = ta.get_df_ended_time_avg()
    resDic["df_ended_time_avg"] = common.transformDfIntoArr(df1)
    fileName = "project_index.xls"
    sheetName = "df_ended_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_ended_time_avg calculate finished！")

    df1 = ta.get_df_opened_time_avg()
    resDic["df_opened_time_avg"] = common.transformDfIntoArr(df1)
    fileName = "project_index.xls"
    sheetName = "df_opened_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_opened_time_avg calculate finished！")


    df1 = ta.get_df_note_time_avg()
    resDic["df_note_time_avg"] = common.transformDfIntoArr(df1)
    fileName = "project_index.xls"
    sheetName = "df_note_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_note_time_avg calculate finished！")

#     timeSpan
    #评审挂起数
    ts = TimeSpan(cProject_list, DATE)
    df = ts.get_df_no_note_count()
    arr = common.transformDfIntoArr(df)
    resArr = transformDicKey(arr)
    resDic["df_no_note_count"] = resArr
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "df_no_note_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    # df['date'] = columns
    # df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("df_no_note_count calculate finished！")


    df = ts.get_df_has_note_count()
    resDic["df_has_note_count"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "df_has_note_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    # df['date'] = columns
    # df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("df_has_note_count calculate finished！")


    df = ts.get_df_ended_count()
    resDic["df_ended_count"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "df_ended_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    # df['date'] = columns
    # df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("df_ended_count calculate finished！")

    # mrRate
    mrRate = MergeRequestRate(cProject_list, DATE)
    df = mrRate.get_df_closed_rate()
    resDic["mrClosedRatio"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrClosedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_opened_rate()
    resDic["mrOpenedRatio"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrOpenedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_merged_rate()
    resDic["mrMergedRatio"] = common.transformDfIntoArr(df)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrMergedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("all finished！")
    return resDic



def transformDicKey(arr=[]):
    resArr = []
    for dic in arr:
        resDic = {}
        for k, v in dic.items():
            kk = k.split('-')[0] + "-" +  k.split('-')[1]
            if kk in resDic.keys():
                resDic[kk] += v
            else:
                resDic[kk] = v
        resArr.append(resDic)
    return resArr


if __name__ == "__main__":
    runAllIndex(["tezos"], (2019,10,2020,10))



