#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/15 19:57
# @Author : NJU
# @Version：V 0.1
# @File : commentAcceptRate.py
# @desc :
import os
import time

import pandas
from pandas import DataFrame

from analyzeData import common
from source.config.projectConfig import projectConfig
from source.utils.ExcelHelper import ExcelHelper
from source.utils.pandas.pandasHelper import pandasHelper
import matplotlib.pyplot as plt


class commentAcceptRate:
    """专门用于计算评审意见认可度的工具函数"""

    @staticmethod
    def commentAcceptRatioByProject(projects, date):
        """计算以项目为粒度的评审意见认可度，通过时间来划分
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

            # x = range(-2, 11)
            # y = []
            # for i in x:
            #     y.append(df_notes.loc[df_notes['change_trigger'] == i].shape[0])
            # plt.bar(x=x, height=y)
            # plt.title(f'review comment({project})')
            # for a, b in zip(x, y):
            #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=11)
            #
            # print("review comment useful:", df_notes.shape[0] - df_notes.loc[df_notes['change_trigger'] < 0].shape[0])
            # plt.show()

            data = pandas.merge(left=df_notes, right=df_mr, left_on="merge_request_id", right_on="iid")
            data['label'] = data["created_at_y"].apply(lambda x: (time.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")))
            data['label_y'] = data['label'].apply(lambda x: x.tm_year)
            data['label_m'] = data['label'].apply(lambda x: x.tm_mon)

            data = data.loc[data["change_trigger"] != -2].copy(deep=True)

            # pandasHelper.writeTSVFile("comment.csv", df_notes)

            # """按照时间拆分"""
            # minYear = min(data['label']).tm_year
            # minMonth = min(data['label']).tm_mon
            # maxYear = max(data['label']).tm_year
            # maxMonth = max(data['label']).tm_mon
            # date = (minYear, minMonth, maxYear, maxMonth)
            tempDict = {"project": project}

            for i in range(date[0] * 12 + date[1], date[2] * 12 + date[3] + 1):  # 拆分的数据做拼接
                y = int((i - i % 12) / 12)
                m = i % 12
                if m == 0:
                    m = 12
                    y = y - 1

                df = data.loc[(data['label_y'] == y) & (data['label_m'] == m)].copy(deep=True)
                commentCount = df.shape[0]
                if commentCount == 0:
                    pass
                else:
                    validCount = df.loc[df['change_trigger'] >= 0].shape[0]
                    t = common.getTimeLableFromTime([(y, m)])[0]
                    # tempDict[f'{y}年{m}月'] = validCount / commentCount
                    tempDict[t] = validCount / commentCount
            result_df = result_df.append(tempDict, ignore_index=True)

            print(result_df.shape)
            # result_df.to_excel("q5_change_trigger_ratio.xls")

        return result_df

    @staticmethod
    def commentAcceptRatioByReviewer(project):
        """计算以项目为粒度的评审意见认可度，通过时间来划分"""
        df_notes = common.getNotesDataFrameByProject(project)
        df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
        df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)
        print(df_notes.shape)

        df_mr = common.getMergeRequestDataFrameByProject(project)

        """日期修补"""
        for index, row in df_mr.iterrows():
            if row["created_at"] is None:
                row["created_at"] = row["merged_at"]

        df_mr = df_mr[["iid", "created_at"]].copy(deep=True)
        df_mr["iid"] = df_mr["iid"].apply(lambda x: int(x))
        df_mr.drop_duplicates(subset=['iid'], inplace=True)

        print(df_mr.shape)

        # x = range(-2, 11)
        # y = []
        # for i in x:
        #     y.append(df_notes.loc[df_notes['change_trigger'] == i].shape[0])
        # plt.bar(x=x, height=y)
        # plt.title(f'review comment({project})')
        # for a, b in zip(x, y):
        #     plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=11)
        #
        # print("review comment useful:", df_notes.shape[0] - df_notes.loc[df_notes['change_trigger'] < 0].shape[0])
        # plt.show()

        data = pandas.merge(left=df_notes, right=df_mr, left_on="merge_request_id", right_on="iid")
        data['label'] = data["created_at_y"].apply(lambda x: (time.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")))
        data['label_y'] = data['label'].apply(lambda x: x.tm_year)
        data['label_m'] = data['label'].apply(lambda x: x.tm_mon)

        data = data.loc[data["change_trigger"] != -2].copy(deep=True)

        # pandasHelper.writeTSVFile("comment.csv", df_notes)

        """按照每个人分类"""
        groups = dict(list(data.groupby('reviewer')))
        # 获取目标语料（即经过自定义分词后的语料）

        date = (2019, 5, 2020, 6)

        columns = ["reviewer"]
        for i in range(date[0] * 12 + date[1], date[2] * 12 + date[3] + 1):  # 拆分的数据做拼接
            y = int((i - i % 12) / 12)
            m = i % 12
            if m == 0:
                m = 12
                y = y - 1
            columns.append(str(f"{y}年{m}月"))

        ratio_df = DataFrame(columns=columns)

        # reviewer_list = ["bidinger", "mbouaziz", "raphael-proust", "romain.nl", "vect0r", "rafoo_"]
        reviewer_list = []
        for reviewer, temp_df in groups.items():
            print(reviewer, temp_df.shape[0])
            if reviewer not in reviewer_list:
                tempDict = {"reviewer": reviewer}
                for i in range(date[0] * 12 + date[1], date[2] * 12 + date[3] + 1):  # 拆分的数据做拼接
                    y = int((i - i % 12) / 12)
                    m = i % 12
                    if m == 0:
                        m = 12
                        y = y - 1

                    df = temp_df.loc[(temp_df['label_y'] == y) & (temp_df['label_m'] == m)].copy(deep=True)
                    sum = df.shape[0]
                    if sum == 0:
                        pass
                        # tempDict[f'{y}年{m}月'] = 0
                    else:
                        valid = df.loc[df['change_trigger'] >= 0].shape[0]
                        tempDict[f'{y}年{m}月'] = valid / sum
                ratio_df = ratio_df.append(tempDict, ignore_index=True)

        print(ratio_df.shape)
        # ratio_df.to_excel("q5_change_trigger_ratio.xls")


if __name__ == "__main__":
    df = commentAcceptRate.commentAcceptRatioByProject(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12))
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "commentAcceptRatio"
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
