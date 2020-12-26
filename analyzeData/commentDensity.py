#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import time

from pandas import DataFrame

import analyzeData.common as common
import csv


# 计算评审意见密度
class commentDensity:
    """用于计算评审意见密度
       需要先调用 calculateCommentDensityByProject
       然后再获得对应的df
    """

    def __init__(self):
        self.notesChangesDensityByProjectDf = None
        self.notesFilesDensityByProjectDf = None

    def calCommentDensity(self, project) -> dict:
        notesMap = common.getNotesMap(project)
        mergeRequestMap = common.getMergeRequestMap(project)
        # 存放最终结果的字典，键是iid，值是一个数组，存放MergeRequest中的notes和changes和file_count的数量
        data = {}
        for iid, mr in mergeRequestMap.items():
            # 可能存在mergeRequest中的iid不在notes文件中
            # 但是依旧需要返回，因为需要算比例   2020.11.16
            createdAt = time.strptime(mr.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            """返回五元组
               [mr中notes数量, mr改动的代码行数, mr改动的文件行数, mr创建的年, mr创建的月]
            """
            if iid not in notesMap:
                data[iid] = [0, mr.changes, mr.file_count, createdAt.tm_year, createdAt.tm_mon]
                continue
            arr = [len(notesMap[iid]), mr.changes, mr.file_count, createdAt.tm_year, createdAt.tm_mon]
            data[iid] = arr
        return data

    def calculateCommentDensityByProject(self, projects, date):
        """提供项目名字列表和日期，保存dataframe到对象中"""
        columns = ["project"]
        # columns.extend([str(f"{y}/{m}") for y, m in common.getTimeListFromTuple(date)])
        timeList = common.getTimeListFromTuple(date)
        columns.extend(common.getTimeLableFromTime(timeList))
        changes_density_df = DataFrame(columns=columns)  # 初始化两个dataframe
        files_density_df = DataFrame(columns=columns)

        for p in projects:
            """通过dict的方式给dataframe 添加项"""
            changesDensityDict = {"project": p}
            filesDensityDict = {"project": p}
            data = self.calCommentDensity(p)
            for y, m in common.getTimeListFromTuple(date):
                """找出每个时间段的mr"""
                totalNotesCount = 0  # 累积一个月的评论数
                totalChangesCount = 0  # 累积一个月的改动代码行数量
                totalFilesCount = 0  # 累积一个月的改动文件数量
                for notesCount, changes, filesCount, createdYear, createdMonth in data.values():
                    if createdYear == y and createdMonth == m:
                        totalNotesCount += notesCount
                        totalChangesCount += changes
                        totalFilesCount += filesCount
                key = common.getTimeLableFromTime([(y, m)])[0]
                if totalNotesCount > 0:
                    changesDensityDict[key] = totalChangesCount / totalNotesCount
                    filesDensityDict[key] = totalFilesCount / totalNotesCount
            changes_density_df = changes_density_df.append(changesDensityDict, ignore_index=True)
            files_density_df = files_density_df.append(filesDensityDict, ignore_index=True)

        self.notesChangesDensityByProjectDf = changes_density_df
        self.notesFilesDensityByProjectDf = files_density_df

    def getNotesChangesDensityByProject(self):
        return self.notesChangesDensityByProjectDf

    def getNotesFilesDensityByProject(self):
        return self.notesFilesDensityByProjectDf


if __name__ == '__main__':
    d = commentDensity()
    d.calculateCommentDensityByProject(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12))
    changes_density_df = d.getNotesChangesDensityByProject()
    print(changes_density_df)
    files_density_df = d.getNotesFilesDensityByProject()
    print(files_density_df)