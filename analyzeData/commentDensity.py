#!/usr/bin/env python
# _*_ coding: utf-8 _*_


import common
import csv

#计算评审意见密度


class MergeRequest:
    '''解析mergeRequest.tsv需要映射的类'''
    def __init__(self, iid, changes, file_count):
        self.iid = iid
        self.changes = changes
        self.file_count = file_count

class Notes:
    def __init__(self, merge_request_id):
        self.merge_request_id = merge_request_id


#读取mergeReques.tsv文件
def readMergeRequestTsvFile(fileName="") -> dict:
    #键是iid，值是mergeRequest对象
    mergeRequestMap = {}
    with open(fileName, 'r', encoding='unicode_escape') as mr_tsv:
        tsv_reader = csv.reader(mr_tsv, delimiter='\t')
        #读取第一行
        tsv_labels = tsv_reader.__next__()
        for record in tsv_reader:
            if len(record) == 0:
                continue
            iid = record[tsv_labels.index("iid")]
            changes = record[tsv_labels.index("changes")]
            file_count = record[tsv_labels.index("file_count")]
            if iid == '' or changes == '':
                continue
            mergeRequest = MergeRequest(iid, changes, file_count)
            mergeRequestMap[iid] = mergeRequest
    return mergeRequestMap


#读取notes.tsv文件
def readNotesTsvFile(fileName="") -> dict:
    #字典的键是merge_request_id，值是一个存放这个mr的所有的notes的数组
    notesMap = {}
    with open(fileName, 'r', encoding='unicode_escape') as notes_tsv:
        tsv_reader = csv.reader(notes_tsv, delimiter='\t')
        tsv_labels = tsv_reader.__next__()
        for record in tsv_reader:
            if len(record) == 0:
                continue
            created_at = record[tsv_labels.index("created_at")]
            merge_request_id = record[tsv_labels.index("merge_request_id")]
            if created_at == '' or merge_request_id == '':
                continue
            notes = Notes(merge_request_id)
            if merge_request_id in notesMap:
                notesList = notesMap[merge_request_id]
                notesList.append(notes)
            else:
                notesList = []
                notesList.append(notes)
                notesMap[merge_request_id] = notesList
    return notesMap


def calCommentDensity() -> dict:
    notesMap = readNotesTsvFile(common.notesTsv)
    mergeRequestMap = readMergeRequestTsvFile(common.mergeRequestTsv)
    #存放最终结果的字典，键是iid，值是一个数组，存放MergeRequest中的notes和changes和file_count的数量
    data = {}
    for iid, mr in mergeRequestMap.items():
        #可能存在mergeRequest中的iid不在notes文件中
        if iid not in notesMap:
            continue
        arr = []
        arr.append(len(notesMap[iid]))
        arr.append(mr.changes)
        arr.append(mr.file_count)
        data[iid] = arr
    return data
if __name__ == '__main__':
    res = calCommentDensity()
    for k, v in res.items():
        print(k, v)
