import csv
from source.data.bean import MergeRequest, Notes
import source.utils.pandas.pandasHelper as pandasHelper
import os
import source.config.projectConfig as projectConfig
from source.data.service.BeanParserHelper import BeanParserHelper

# 文件路径
mergeRequestTsv = "../data/file/mergeRequest.tsv"
notesTsv = "../data/file/notes.tsv"


# 返回以iid为键的存放MergeRequest的字典
def getMergeRequestMap() -> dict:
    # 键是iid，值是mergeRequest对象
    mergeRequestMap = {}
    mergeRequestList = getMergeRequestInstances("data/file/mergeRequest/mergeRequest.tsv")

    for mergeRequest in mergeRequestList:
        iid = mergeRequest.iid
        created_at = mergeRequest.created_at
        if iid == '' or created_at == '':
            continue
        mergeRequestMap[iid] = mergeRequest
    return mergeRequestMap


# 返回以merge_request_id为键，值为这个mergeRequest中所有notes的数组的字典
def getNotesMap() -> dict:
    # 字典的键是merge_request_id，值是一个存放这个mergeRequest的所有的notes的数组
    notesMap = {}
    notesList = getNotesInstances("notes.tsv")
    for notes in notesList:
        created_at = notes.created_at
        merge_request_id = notes.merge_request_id
        if created_at == '' or merge_request_id == '':
            continue
        if merge_request_id in notesMap:
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
    df = pandasHelper.pandasHelper.readTSVFile(
        projectConfig.projectConfig.getMergeRequestDataPath() + os.sep + f"mergeRequest_{project}.tsv",
        header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)

    # 处理空行
    df.dropna(subset=["id"], inplace=True)

    for index, row in df.iterrows():
        t = tuple(row)
        bean = BeanParserHelper.getBeansFromTuple(MergeRequest.MergeRequest(),
                                                  MergeRequest.MergeRequest.getItemKeyList(), t)
        res.extend(bean)
    return res


# 传入要读取的文件名，返回实例化好的Notes数组
def getNotesInstances(project) -> []:
    res = []
    df = pandasHelper.pandasHelper.readTSVFile(
        projectConfig.projectConfig.getNotesDataPath() + os.sep + f"notes_{project}.tsv",
        header=pandasHelper.pandasHelper.INT_READ_FILE_WITH_HEAD)

    # 处理空行
    df.dropna(subset=["id"], inplace=True)

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
