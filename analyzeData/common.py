import calendar
import csv
import time

import numpy
import pandas
from pandas import DataFrame
import datetime

from pandas._libs.tslib import Timestamp

from source.data.bean import MergeRequest, Notes
import source.utils.pandas.pandasHelper as pandasHelper
import os
import source.config.projectConfig as projectConfig
from source.data.service.BeanParserHelper import BeanParserHelper

# 文件路径
from source.utils.ExcelHelper import ExcelHelper

mergeRequestTsv = "../data/file/mergeRequest.tsv"
notesTsv = "../data/file/notes.tsv"


def getMergeRequestDataFrameByProject(project) -> DataFrame:
    # 通用的获取项目数据的接口，所有的指标都是从这个接口拿MergeRequest数据，便于后续服务化  2020.12.14
    if os.path.exists(projectConfig.projectConfig.getMergeRequestDataPath() + os.sep + f"mergeRequest_{project}.tsv"):
        df = pandasHelper.pandasHelper.readTSVFile(
            projectConfig.projectConfig.getMergeRequestDataPath() + os.sep + f"mergeRequest_{project}.tsv",
            header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)
    else:
        df = pandas.DataFrame(columns=MergeRequest.MergeRequest.getItemKeyList())
    return df


def getNotesDataFrameByProject(project) -> DataFrame:
    # 通用的获取项目数据的接口，所有的指标都是从这个接口拿Notes数据，便于后续服务化  2020.12.14
    if os.path.exists(projectConfig.projectConfig.getNotesDataPath() + os.sep + f"notes_{project}.tsv"):
        df = pandasHelper.pandasHelper.readTSVFile(
            projectConfig.projectConfig.getNotesDataPath() + os.sep + f"notes_{project}.tsv",
            header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)
    else:
        df = pandas.DataFrame(columns=Notes.Notes.getItemKeyList())
    return df


# 返回以iid为键的存放MergeRequest的字典
def getMergeRequestMap(project) -> dict:
    # 键是iid，值是mergeRequest对象
    mergeRequestMap = {}
    mergeRequestList = getMergeRequestInstances(project)

    for mergeRequest in mergeRequestList:
        iid = mergeRequest.iid
        created_at = mergeRequest.created_at
        if iid == '' or created_at == '' or isinstance(created_at, float):
            continue
        mergeRequestMap[iid] = mergeRequest
    return mergeRequestMap


# 返回以merge_request_id为键，值为这个mergeRequest中所有notes的数组的字典
def getNotesMap(project) -> dict:
    # 字典的键是merge_request_id，值是一个存放这个mergeRequest的所有的notes的数组
    notesMap = {}
    notesList = getNotesInstances(project)
    for notes in notesList:
        created_at = notes.created_at
        merge_request_id = notes.merge_request_id
        change_trigger = notes.change_trigger
        """新增  去除作者自己的评论  change_trigger == -2  @张逸凡  2020.11.16"""
        if created_at == '' or merge_request_id == '' or change_trigger == -2 or isinstance(created_at, float):
            continue
        if merge_request_id in notesMap.keys():  # 容易造成歧义
            notesList = notesMap[merge_request_id]
            notesList.append(notes)
        else:
            notesList = []
            notesList.append(notes)
            notesMap[merge_request_id] = notesList
    return notesMap


# 传入文件名，返回实例化好的mergeRequest数组
def getMergeRequestInstances(project) -> []:
    res = []
    df = getMergeRequestDataFrameByProject(project)

    # 处理空行
    df.dropna(subset=["id", "created_at"], inplace=True)

    # 需要注意重复数据的情况
    df.drop_duplicates(subset=["iid"], inplace=True)

    if df.shape[0] > 0:
        # 去除状态为closed并且closedtime为空的异常数据
        df['closed_error_label'] = df.apply(lambda x: x["state"] == "closed" and isinstance(x["closed_at"], float),
                                            axis=1)
        df = df.loc[df['closed_error_label'] == 0].copy(deep=True)
        df.drop(['closed_error_label'], axis=1, inplace=True)

        # 去除状态为closed并且closedtime小于createTime的异常数据
        df['closed_error_label'] = df.apply(lambda x: x["state"] == "closed" and x["closed_at"] < x["created_at"],
                                            axis=1)
        df = df.loc[df['closed_error_label'] == 0].copy(deep=True)
        df.drop(['closed_error_label'], axis=1, inplace=True)

        # 去除状态为merged并且mergedtime为空的异常数据
        df['merged_error_label'] = df.apply(lambda x: x["state"] == "merged" and isinstance(x["merged_at"], float),
                                            axis=1)
        df = df.loc[df['merged_error_label'] == 0].copy(deep=True)
        df.drop(['merged_error_label'], axis=1, inplace=True)

    for index, row in df.iterrows():
        t = tuple(row)
        bean = BeanParserHelper.getBeansFromTuple(MergeRequest.MergeRequest(),
                                                  MergeRequest.MergeRequest.getItemKeyList(), t)
        res.extend(bean)
    return res


# 传入要读取的文件名，返回实例化好的Notes数组
def getNotesInstances(project) -> []:
    res = []
    df = getNotesDataFrameByProject(project)

    # 处理空行
    df.dropna(subset=["id"], inplace=True)
    # 处理重复
    df.drop_duplicates(subset=["id"], inplace=True)

    for index, row in df.iterrows():
        t = tuple(row)
        bean = BeanParserHelper.getBeansFromTuple(Notes.Notes(), Notes.Notes.getItemKeyList(), t)
        res.extend(bean)
    return res


def getTimeListFromTuple(date):
    """输入一个时间的四元组，返回一个时间列表
       如输入: (2020, 1, 2020, 2)
       输出：[(2020,1),(2020,2)]
    """
    timeList = []
    for i in range(date[0] * 12 + date[1], date[2] * 12 + date[3] + 1):
        y = int((i - i % 12) / 12)
        m = i % 12
        if m == 0:
            m = 12
            y = y - 1
        timeList.append((y, m))
    return timeList


def getDayTimeListFromTuple(date):
    timeList = []
    start_date = datetime.date(date[0], date[1], date[2])
    end_date = datetime.date(date[3], date[4], date[5])
    for n in date_range(start_date, end_date):
        timeList.append((n.year, n.month, n.day))
    return timeList


def date_range(start_date, end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + datetime.timedelta(n)


def getVersionFromTuple(dateList):
    """输入一个[(v2, (2020, 1,1,2020,2,1))]的列表，返回版本列表和映射map
       如输入: [(v2, (2020, 1,1,2020,2,1))]
       输出：["v2"],{"v2":(2020, 1, 1, 2020, 2 1)}
    """
    versionList = []
    timeMap = {}
    for v, date in dateList:
        versionList.append(v)
        timeMap[v] = date
    return versionList, timeMap


def checkDateTimeInGap(targetTime, gap):
    startYear, startMonth, startDay, endYear, endMonth, endDay = gap
    startTime = time.strptime(f"{startYear}-{startMonth}-{startDay}", "%Y-%m-%d")
    endTime = time.strptime(f"{endYear}-{endMonth}-{endDay}", "%Y-%m-%d")
    return startTime < targetTime <= endTime  # 左不含，右含


# 检查给定时间是否晚于限制时间
def checkTimeIsMoreThan(time=datetime.datetime, timeLimit=()) -> bool:
    # 时间上限
    yearUp = timeLimit[2]
    monthUp = timeLimit[3]

    year = time.year
    month = time.month
    if year > yearUp:
        return True
    elif year == yearUp:
        if month > monthUp:
            return True
        else:
            return False
    else:
        return False


# 检查时间是否早于限制时间
def checkTimeIsLessThan(time=datetime.datetime, timeLimit=()) -> bool:
    year = time.year
    month = time.month

    # 时间下限
    yearDown = timeLimit[0]
    monthDown = timeLimit[1]

    if year < yearDown:
        return True
    elif year == yearDown:
        if month < monthDown:
            return True
        else:
            return False
    else:
        return False


# 判断传入的时间是否符合时间限制
def checkTime(time=datetime.datetime, timeLimit=()) -> bool:
    if not isinstance(time, datetime.datetime):  # 新增类型判断 2020.12.30
        return False
    if checkTimeIsMoreThan(time, timeLimit):
        return False
    elif checkTimeIsLessThan(time, timeLimit):
        return False
    else:
        return True


# 把字符串转成Datetime格式
def tranformStrToDateTime(timeStr='') -> datetime.datetime:
    try:
        if '.' in timeStr:
            timeStr = timeStr.split(".")[0]
        else:
            timeStr = timeStr[:-1]
        timeArray = datetime.datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
    except:
        print(timeStr)
    return timeArray


def getDayListFromTuple(date):
    """输入一个时间的四元组，返回一个时间列表,粒度精确到日期
       如输入: (2020, 1, 2020, 2)
       输出：[(2020,1,1),(2020,1,2), ........(2020, 1, 31)]
    """
    timeList = []
    for i in range(date[0] * 12 + date[1], date[2] * 12 + date[3] + 1):
        y = int((i - i % 12) / 12)
        m = i % 12
        if m == 0:
            m = 12
            y = y - 1
        weekDay, totalDay = calendar.monthrange(y, m)
        for d in range(1, totalDay + 1):
            timeList.append((y, m, d))
    return timeList


def getTimeLableFromTime(time_list):
    """
    输入一个时间列表，输出时间字符串列表
    如输入：[(2020,9),(2020,10)]
    输出：[2020-09,2020-10]
    """

    time_label = []
    for time in time_list:
        timeStr = str(time[0])
        if time[1] < 10:
            timeStr = timeStr + "-0" + str(time[1])
        else:
            timeStr = timeStr + "-" + str(time[1])
        time_label.append(timeStr)

    return time_label


def getDayLabelFromTime(time_list):
    """
    输入一个时间列表，输出时间字符串列表
    如输入：[(2020,9),(2020,10)]
    输出：[2020-09,2020-10]
    """

    time_label = []
    for time in time_list:
        timeStr = str(time[0])
        if time[1] < 10:
            timeStr = timeStr + "-0" + str(time[1])
        else:
            timeStr = timeStr + "-" + str(time[1])
        if time[2] < 10:
            timeStr = timeStr + "-0" + str(time[2])
        else:
            timeStr = timeStr + "-" + str(time[2])
        time_label.append(timeStr)

    return time_label


def getParticipantCount(project, date):
    """给定一个项目名字 和时间范围四元组
    返回项目涉及参与开发的人数"""
    df_notes = getNotesDataFrameByProject(project)
    df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
    df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)

    df_mr = getMergeRequestDataFrameByProject(project)
    df_mr.dropna(subset=["iid"], inplace=True)

    """日期修补"""
    for index, row in df_mr.iterrows():
        if row["created_at"] is None:
            row["created_at"] = row["merged_at"]

    df_mr = df_mr[["iid", "created_at", 'author_user_name']].copy(deep=True)
    df_mr["iid"] = df_mr["iid"].apply(lambda x: int(x))
    df_mr.drop_duplicates(subset=['iid'], inplace=True)

    data = pandas.merge(left=df_notes, right=df_mr, left_on="merge_request_id", right_on="iid")
    data['label'] = data["created_at_y"].apply(lambda x: tranformStrToDateTime(x))  # 用日期转化的兼容方法
    data['label'] = data["label"].apply(lambda x: checkTime(x, date))  # 过滤时间段
    data = data.loc[data['label'] == 1].copy(deep=True)

    print(data.shape)
    userList = []  # 统计参与用户列表
    userList.extend(data['author_user_name_x'])
    userList.extend(data['author_user_name_y'])
    userList = list(set(userList))
    return userList.__len__()


def modifyIndexByProjectUserScale(filename, sheetname, date):
    """提供一个excel文件和对应的sheet名称.
       提供希望统计项目人数的时间范围，
    对目标sheet上面的指标做人数的加权处理(现在是人数的相除)"""

    # 注： 要结合指标的场景使用，必须是常用的条状excel表格可以计算
    # 现在由于解决项目稀疏问题，人为的指定项目的时间范围

    sheet = ExcelHelper().readExcelSheet(filename, sheetname)
    print(sheet)

    nrows = sheet.nrows
    ncols = sheet.ncols
    cols = sheet.row_values(0)
    df = pandas.DataFrame(columns=cols)

    # 先统计项目参与人数加权
    projectList = []  # 项目名字列表
    projectScaleList = []  # 项目参与人数列表
    projectRatioList = []  # 加权因子列表
    maxNum = -1
    for i in range(1, nrows):
        project = sheet.cell(i, 0).value
        projectList.append(project)
        projectScale = getParticipantCount(project, date)
        if maxNum < projectScale:
            maxNum = projectScale
        projectScaleList.append(projectScale)

    """先人数归一化，作为x计算   
       =>  e^(-x)
    """

    for index, project in enumerate(projectList):
        ratio = projectScaleList[index] / maxNum
        ratio = numpy.exp(-1 * ratio)
        projectRatioList.append(ratio)

    for i in range(1, nrows):
        row = sheet.row_values(i)
        print(row)
        tempDict = {cols[0]: row[0]}
        for j in range(1, ncols):
            v = row[j]
            if v != "" and not numpy.isnan(v):
                tempDict[cols[j]] = v * projectRatioList[i - 1]
            else:
                tempDict[cols[j]] = v  # 否则不变
        df = df.append(tempDict, ignore_index=True)
    print(df.shape)

    # 添加结果到新的sheet
    newSheetName = f"{sheetname}_ratio"
    ExcelHelper().writeDataFrameToExcel(filename, newSheetName, df)


if __name__ == "__main__":
    # getParticipantCount('tezos', (2019, 9, 2020, 11))
    filename = projectConfig.projectConfig.getRootPath() + os.sep + 'analyzeData' + os.sep + 'project_index.xls'
    modifyIndexByProjectUserScale(filename, 'commentAcceptRatio', (2019, 9, 2020, 11))
