from analyzeData.calReplyTime import classifyByTimeByProject
from analyzeData.commentAcceptRate import commentAcceptRate
from analyzeData.commentDistribution import commentDistribution
from analyzeData.mrRate import MergeRequestRate
from analyzeData.timeAvg import TimeAvg
from analyzeData.timeSpan import TimeSpan
from source.utils.ExcelHelper import ExcelHelper
import pandas
import pandas as pd
import datetime
import xlrd as xlrd
from source.utils.StringKeyUtils import StringKeyUtils as sku

DATE = (2019, 9, 2020, 11)


def getDataFromExcel():
    excel = xlrd.open_workbook(r'PPS9个服务去重整理.xlsx')
    sheet = excel.sheet_by_name('de_duplicates')
    spnameList = sheet.col_values(2)[1:]
    dic = {}
    for spname in spnameList:
        dic[spname] = 1
    return list(dic.keys())


if __name__ == '__main__':

    cProject_list = getDataFromExcel()

    # cProject_list = ["Attributionservice_PPSAttributionService_Commons"]


    df = commentAcceptRate.commentAcceptRatioByProject(cProject_list, DATE)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentAcceptRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentAcceptRatio calculate finished！")

    baseDf = commentDistribution.commentDistributionByProject(cProject_list, DATE)
    """时间和周的交叉详细统计，描述看文档"""
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentDistributionALL"
    # print(df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, baseDf)
    print("commentDistributionALL calculate finished！")

    df = commentDistribution.commentDistributionByProjectWithWeekDay(cProject_list, DATE, baseDf)
    """周的单独统计，描述看文档"""
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentDistributionByWeekday"
    # print(df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByWeekday calculate finished！")

    df = commentDistribution.commentDistributionByProjectWithInterval(cProject_list, DATE, baseDf)
    """时间的单独统计，描述看文档"""
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentDistributionByInterval"
    # print(df)
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("commentDistributionByInterval calculate finished！")

    df = classifyByTimeByProject(cProject_list, DATE)
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "calReplyTime"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    print("calReplyTime calculate finished！")

    # time avg
    ta = TimeAvg(cProject_list, DATE)
    df1 = ta.get_df_ended_time_avg()
    fileName = "project_index.xls"
    sheetName = "df_ended_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_ended_time_avg calculate finished！")

    df1 = ta.get_df_opened_time_avg()
    fileName = "project_index.xls"
    sheetName = "df_opened_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_opened_time_avg calculate finished！")


    df1 = ta.get_df_note_time_avg()
    fileName = "project_index.xls"
    sheetName = "df_note_time_avg"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df1)
    print("df_note_time_avg calculate finished！")

#     timeSpan
    ts = TimeSpan(cProject_list, DATE)
    df = ts.get_df_no_note_count()
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
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrClosedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_opened_rate()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrOpenedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_merged_rate()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrMergedRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    print("all finished！")



