#!/usr/bin/env python
# _*_ coding: utf-8 _*_


import common
import csv


#计算评审意见密度



def calCommentDensity() -> dict:
    notesMap = common.getNotesMap()
    mergeRequestMap = common.getMergeRequestMap()
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
