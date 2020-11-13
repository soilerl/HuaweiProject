import csv
import json
from source.data.bean import MergeRequest, Notes

#文件路径
mergeRequestTsv = "../data/file/mergeRequest.tsv"
notesTsv = "../data/file/notes.tsv"


def readTsvFile(fileName='', encoding='unicode_escape') -> list:
    """读取csv文件，返回一个存字典的数组，将每一行数据转换成字典"""
    res = []
    with open(fileName, 'r', encoding=encoding) as tsv:
        tsv_reader = csv.reader(tsv, delimiter='\t')
        tsv_labels = tsv_reader.__next__()
        for record in tsv_reader:
            if len(record) == 0:
                continue
            if len(record[0]) == 0:
                continue
            recordMap = {}
            for i in range(1, len(tsv_labels)):
                recordMap[tsv_labels[i]] = record[i]
            res.append(recordMap)
    return res

def getMergeRequestInstanceList(mergeRequestArr=[]) -> []:
    """根据参数返回赋值完毕的mergeRequest实例列表"""
    res = []
    for mergeRequestDict in mergeRequestArr:
        mergeRequest = MergeRequest.MergeRequest.parser.parser(mergeRequestDict)
        res.append(mergeRequest)
    return res

def getNotesInstanceList(notesArr=[]) -> []:
    """根据参数返回赋值完毕的notes实例列表"""
    res = []
    for notesDict in notesArr:
        notes = Notes.Notes.parser.parser(notesDict)
        res.append(notes)
    return res

