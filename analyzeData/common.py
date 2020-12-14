import csv

import numpy
from pandas import DataFrame

from source.data.bean import MergeRequest, Notes
import source.utils.pandas.pandasHelper as pandasHelper
import os
import source.config.projectConfig as projectConfig
from source.data.service.BeanParserHelper import BeanParserHelper

# 文件路径
mergeRequestTsv = "../data/file/mergeRequest.tsv"
notesTsv = "../data/file/notes.tsv"


def getMergeRequestDataFrameByProject(project) -> DataFrame:
    # 通用的获取项目数据的接口，所有的指标都是从这个接口拿MergeRequest数据，便于后续服务化  2020.12.14
    df = pandasHelper.pandasHelper.readTSVFile(
        projectConfig.projectConfig.getMergeRequestDataPath() + os.sep + f"mergeRequest_{project}.tsv",
        header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)
    return df


def getNotesDataFrameByProject(project) -> DataFrame:
    # 通用的获取项目数据的接口，所有的指标都是从这个接口拿Notes数据，便于后续服务化  2020.12.14
    df = pandasHelper.pandasHelper.readTSVFile(
        projectConfig.projectConfig.getNotesDataPath() + os.sep + f"notes_{project}.tsv",
        header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)
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

    # 去除状态为closed并且closedtime为空的异常数据
    df['closed_error_label'] = df.apply(lambda x: x["state"] == "closed" and isinstance(x["closed_at"], float), axis=1)
    df = df.loc[df['closed_error_label'] == 0].copy(deep=True)
    df.drop(['closed_error_label'], axis=1, inplace=True)

    # 去除状态为merged并且mergedtime为空的异常数据
    df['merged_error_label'] = df.apply(lambda x: x["state"] == "merged" and isinstance(x["merged_at"], float), axis=1)
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


def getTimeLableFromTime(time_list):
    """
    输入一个时间列表，输出时间字符串列表
    如输入：[(2020,9),(2020,10)]
    输出：[2020-09,2020-10]
    """

    time_label = []

    for time in time_list:
        if time[1] < 10:
            time_label.append(str(time[0]) + "-0" + str(time[1]))
        else:
            time_label.append(str(time[0]) + "-" + str(time[1]))

    return time_label
