#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/15 19:57
# @Author : NJU
# @Version：V 0.1
# @File : commentAcceptRate.py
# @desc :
import os
import time

import numpy
import pandas
from pandas import DataFrame

from analyzeData import common
from source.config.projectConfig import projectConfig
from source.utils.ExcelHelper import ExcelHelper
from source.utils.pandas.pandasHelper import pandasHelper


class commentCount:
    """专门用于计算每个月评审意见数量的"""

    @staticmethod
    def commentCountByProject(projects, date):
        """计算以项目为粒度通过时间来划分
           projects: 指定若干的项目
           date: 四元组，指定计算指标的开始时间和结束时间 （minYear, minMonth, maxYear, maxMonth）
           如（2019,10,2020,11） 是闭区间
        """
        columns = ["project"]
        timeList = common.getTimeListFromTuple(date)
        columns.extend(common.getTimeLableFromTime(timeList))

        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        for project in projects:
            df_notes = common.getNotesDataFrameByProject(project)
            df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
            df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)
            print(df_notes.shape)
            #
            # data = df_notes

            df_mr = common.getMergeRequestDataFrameByProject(project)
            df_mr.dropna(subset=["iid"], inplace=True)

            """日期修补"""
            for index, row in df_mr.iterrows():
                if row["created_at"] is None:
                    row["created_at"] = row["merged_at"]

            df_mr = df_mr[["iid", "created_at"]].copy(deep=True)
            df_mr["iid"] = df_mr["iid"].apply(lambda x: int(x))
            df_mr.drop_duplicates(subset=['iid'], inplace=True)

            print(df_mr.shape)

            data = pandas.merge(left=df_notes, right=df_mr, left_on="merge_request_id", right_on="iid")
            data['label'] = data["created_at_y"].apply(lambda x: (time.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")))
            # data['label'] = data["created_at"].apply(lambda x: (time.strptime(x, "%Y-%m-%dT%H:%M:%S.%f%z"))) 华为备用
            data['label_y'] = data['label'].apply(lambda x: x.tm_year)
            data['label_m'] = data['label'].apply(lambda x: x.tm_mon)

            data = data.loc[data["change_trigger"] != -2].copy(deep=True)

            tempDict = {"project": project}

            for y, m in common.getTimeListFromTuple(date):
                df = data.loc[(data['label_y'] == y) & (data['label_m'] == m)].copy(deep=True)
                commentCount = df.shape[0]
                mrCount = list(set(df['iid'])).__len__()
                t = common.getTimeLableFromTime([(y, m)])[0]
                if mrCount > 0:
                    tempDict[t] = commentCount / mrCount
                else:
                    tempDict[t] = numpy.NAN
            result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentCountByProjectVersion(project, dateList):
        """计算以项目为粒度的评审意见数量，通过时间来划分
           project: 指定某个项目
           dateList: 是列表，列表元素
                     有两个部分，第一个部分是版本名字，第二个部分是时间六元组
                     四元组，指定计算指标的开始时间和结束时间 （minYear, minMonth, minDay, maxYear, maxMonth, minDay）
                     [("v1", (2020, 1, 1, 2020, 2, 1)), ("v2", (2020, 2, 1, 2020, 3, 1))]
        """
        columns = ["project"]

        versionList, timeMap = common.getVersionFromTuple(dateList)
        columns.extend(versionList)
        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        df_notes = common.getNotesDataFrameByProject(project)
        df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
        df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)
        print(df_notes.shape)

        df_mr = common.getMergeRequestDataFrameByProject(project)
        df_mr.dropna(subset=["iid"], inplace=True)

        """日期修补"""
        for index, row in df_mr.iterrows():
            if row["created_at"] is None:
                row["created_at"] = row["merged_at"]

        df_mr = df_mr[["iid", "created_at"]].copy(deep=True)
        df_mr["iid"] = df_mr["iid"].apply(lambda x: int(x))
        df_mr.drop_duplicates(subset=['iid'], inplace=True)

        print(df_mr.shape)

        data = pandas.merge(left=df_notes, right=df_mr, left_on="merge_request_id", right_on="iid")
        data['time'] = data["created_at_y"].apply(lambda x: (time.strptime(x[0:10], "%Y-%m-%d")))
        data = data.loc[data["change_trigger"] != -2].copy(deep=True)

        tempDict = {"project": project}
        for v in versionList:
            df = data.copy(deep=True)
            df['label'] = df["time"].apply(lambda x: common.checkDateTimeInGap(x, timeMap[v]))
            df = df.loc[df['label'] > 0].copy(deep=True)
            commentCount = df.shape[0]
            mrCount = list(set(df['iid'])).__len__()
            if mrCount > 0:
                tempDict[v] = commentCount / mrCount
            else:
                tempDict[v] = numpy.NAN
        result_df = result_df.append(tempDict, ignore_index=True)
        return result_df


if __name__ == "__main__":
    # df = commentCount.commentCountByProject(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12))
    df = commentCount.commentCountByProjectVersion('tezos',  [("v1", (2020, 7, 20, 2020, 9, 1)),
                                                              ("v2", (2020, 9, 1, 2020, 10, 9)),
                                                              ("v3", (2020, 10, 9, 2020, 11, 14)),
                                                              ("v4", (2020, 11, 14, 2020, 12, 4))])
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentCount"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
