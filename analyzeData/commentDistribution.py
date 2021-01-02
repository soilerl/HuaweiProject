#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/15 19:57
# @Author : NJU
# @Version：V 0.1
# @File : commentDistribution.py
# @desc :
import calendar
import os
import time

import pandas
import seaborn
from pandas import DataFrame

from analyzeData import common
from source.utils.ExcelHelper import ExcelHelper
import matplotlib.pyplot as plt


class commentDistribution:
    """专门用于计算评审的日期分布
       按照两个维度来分
       按照周来分  0，1，2，3，4，5，6 （周一 ~ 周日）
       # 按照凌晨早中晚分 0，1，2，3 （0 ~ 6 点，6 ~ 12点， 12 ~ 18 点， 18点 ~ 24点）
       现在直接按照小时划分
    """

    @staticmethod
    def judgeInterval(h):
        """ 用于判断时间间隔的 """
        if 0 <= h < 6:
            return 0
        elif 6 <= h < 12:
            return 1
        elif 12 <= h < 18:
            return 2
        elif 18 <= h <= 24:
            return 3

    @staticmethod
    def commentDistributionByProject(projects, date):
        """计算以项目为粒度通过时间来划分
           projects: 指定若干的项目
           date: 四元组，指定计算指标的开始时间和结束时间 （minYear, minMonth, maxYear, maxMonth）
           如（2019,10,2020,11） 是闭区间
        """
        columns = ["date", "weekday", "interval"]
        columns.extend(projects)

        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        # 建立项目的df_map 用于统计
        df_map = {}
        # 建立频率统计 map，减少查询的耗时
        df_fre_map = {}

        for project in projects:
            df_notes = common.getNotesDataFrameByProject(project)
            df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
            df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)
            print(df_notes.shape)

            df_notes['label'] = df_notes["created_at"].apply(lambda x: (time.strptime(x[0:19], "%Y-%m-%dT%H:%M:%S")))
            df_notes['label_y'] = df_notes['label'].apply(lambda x: x.tm_year)
            df_notes['label_m'] = df_notes['label'].apply(lambda x: x.tm_mon)
            df_notes['label_d'] = df_notes['label'].apply(lambda x: x.tm_mday)
            # df_notes['label_i'] = df_notes['label'].apply(lambda x: commentDistribution.judgeInterval(x.tm_hour))
            df_notes['label_i'] = df_notes['label'].apply(lambda x: x.tm_hour)

            df_notes = df_notes.loc[df_notes["change_trigger"] != -2].copy(deep=True)  # 过滤是作者的情况
            df_map[project] = df_notes

            """遍历df"""
            for index, row in df_notes.iterrows():
                t = (project, row['label_y'], row['label_m'], row['label_d'], row['label_i'])
                if df_fre_map.get(t, None) is None:
                    df_fre_map[t] = 0
                df_fre_map[t] = df_fre_map[t] + 1

        for y, m in common.getTimeListFromTuple(date):
            # 获取某个年月的所有日期
            weekDay, totalDay = calendar.monthrange(y, m)
            for d in range(1, totalDay + 1):
                for i in range(0, 24):  # interval的遍历
                    tempDict = {"date": str((y, m, d)), "weekday": weekDay, "interval": i}
                    for project in projects:
                        r = df_fre_map.get((project, y, m, d, i), 0)
                        tempDict[project] = r
                        # tempDf = df_map[project].copy(deep=True)
                        # tempDf = tempDf.loc[
                        #     (tempDf['label_y'] == y) & (tempDf['label_m'] == m) & (tempDf['label_d'] == d) & (tempDf['label_i'] == i)]
                        # tempDict[project] = tempDf.shape[0]
                    result_df = result_df.append(tempDict, ignore_index=True)
                weekDay = (weekDay + 1) % 7
        return result_df

    @staticmethod
    def commentDistributionByProjectVersion(project, dateList):
        """计算以项目为粒度通过时间来划分
           project: 项目
           dateList: 是列表，列表元素
                     有两个部分，第一个部分是版本名字，第二个部分是时间六元组
                     四元组，指定计算指标的开始时间和结束时间 （minYear, minMonth, minDay, maxYear, maxMonth, minDay）
                     [("v1", (2020, 1, 1, 2020, 2, 1)), ("v2", (2020, 2, 1, 2020, 3, 1))]
        """
        """由于是输出总的时间范围，直接取第一个的起始时间和最后一个的终止时间"""

        columns = ["date", "weekday", "interval", project]

        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        # 建立项目的df_map 用于统计
        df_map = {}
        # 建立频率统计 map，减少查询的耗时
        df_fre_map = {}

        df_notes = common.getNotesDataFrameByProject(project)
        df_notes.drop_duplicates(subset=['id'], inplace=True, keep="last")
        df_notes.sort_values(by='merge_request_id', ascending=False, inplace=True)
        print(df_notes.shape)

        df_notes['label'] = df_notes["created_at"].apply(lambda x: (time.strptime(x[0:19], "%Y-%m-%dT%H:%M:%S")))
        df_notes['label_y'] = df_notes['label'].apply(lambda x: x.tm_year)
        df_notes['label_m'] = df_notes['label'].apply(lambda x: x.tm_mon)
        df_notes['label_d'] = df_notes['label'].apply(lambda x: x.tm_mday)
        # df_notes['label_i'] = df_notes['label'].apply(lambda x: commentDistribution.judgeInterval(x.tm_hour))
        df_notes['label_i'] = df_notes['label'].apply(lambda x: x.tm_hour)

        df_notes = df_notes.loc[df_notes["change_trigger"] != -2].copy(deep=True)  # 过滤是作者的情况
        df_map[project] = df_notes

        """遍历df"""
        for index, row in df_notes.iterrows():
            t = (project, row['label_y'], row['label_m'], row['label_d'], row['label_i'])
            if df_fre_map.get(t, None) is None:
                df_fre_map[t] = 0
            df_fre_map[t] = df_fre_map[t] + 1

        _, startDate = dateList[0]
        _, endDate = dateList[-1]

        targetDate = (startDate[0], startDate[1], startDate[2], endDate[3], endDate[4], endDate[5])
        for y, m, d in common.getDayTimeListFromTuple(targetDate):
            weekDay, totalDay = calendar.monthrange(y, m)
            weekDay = (weekDay + d + 6) % 7
            for i in range(0, 24):  # interval的遍历
                tempDict = {"date": str((y, m, d)), "weekday": weekDay, "interval": i}
                r = df_fre_map.get((project, y, m, d, i), 0)
                tempDict[project] = r
                result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentDistributionByProjectWithWeekDay(projects, date, data=None):
        """在原来的数据上面再加工，提供单独每日分布"""
        columns = ["project", "0", "1", "2", "3", "4", "5", "6"]
        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        if data is None:
            data = commentDistribution.commentDistributionByProject(projects, date)
        print(data)

        df_fre_map = {}  # 用于统计数量
        data = data.copy(deep=True)
        data.drop(columns=['date', 'interval'], inplace=True)
        groups = dict(list(data.groupby(['weekday'])))
        for weekday, df in groups.items():
            weekdayCount = df.sum()
            for p in projects:
                df_fre_map[(p, weekday)] = weekdayCount[p]

        for p in projects:
            tempDict = {"project": p}
            for d in range(0, 7):
                tempDict[str(d)] = df_fre_map.get((p, d), 0)
            result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentDistributionByProjectWithWeekDayVersion(project, dateList, data=None):
        """在原来的数据上面再加工，提供单独每日分布"""
        columns = ["project", "0", "1", "2", "3", "4", "5", "6"]
        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        if data is None:
            data = commentDistribution.commentDistributionByProjectVersion(project, dateList)
        print(data)

        df_fre_map = {}  # 用于统计数量
        data = data.copy(deep=True)
        data.drop(columns=['date', 'interval'], inplace=True)
        groups = dict(list(data.groupby(['weekday'])))
        for weekday, df in groups.items():
            weekdayCount = df.sum()
            df_fre_map[(project, weekday)] = weekdayCount[project]

        tempDict = {"project": project}
        for d in range(0, 7):
            tempDict[str(d)] = df_fre_map.get((project, d), 0)
        result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentDistributionByProjectWithInterval(projects, date, data=None):
        """在原来的数据上面再加工，提供单独每日分布"""
        columns = ["project"]
        columns.extend([str(i) for i in range(0, 24)])
        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        if data is None:
            data = commentDistribution.commentDistributionByProject(projects, date)
        print(data)

        df_fre_map = {}  # 用于统计数量
        data = data.copy(deep=True)
        data.drop(columns=['date', 'weekday'], inplace=True)
        groups = dict(list(data.groupby(['interval'])))
        for interval, df in groups.items():
            weekdayCount = df.sum()
            for p in projects:
                df_fre_map[(p, interval)] = weekdayCount[p]

        for p in projects:
            tempDict = {"project": p}
            for i in range(0, 24):
                tempDict[str(i)] = df_fre_map.get((p, i), 0)
            result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentDistributionByProjectWithIntervalVersion(project, dateList, data=None):
        """在原来的数据上面再加工，提供单独每日分布"""
        columns = ["project"]
        columns.extend([str(i) for i in range(0, 24)])
        result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

        if data is None:
            data = commentDistribution.commentDistributionByProjectVersion(project, dateList)
        print(data)

        df_fre_map = {}  # 用于统计数量
        data = data.copy(deep=True)
        data.drop(columns=['date', 'weekday'], inplace=True)
        groups = dict(list(data.groupby(['interval'])))
        for interval, df in groups.items():
            weekdayCount = df.sum()
            df_fre_map[(project, interval)] = weekdayCount[project]

        tempDict = {"project": project}
        for i in range(0, 24):
            tempDict[str(i)] = df_fre_map.get((project, i), 0)
        result_df = result_df.append(tempDict, ignore_index=True)
        return result_df

    @staticmethod
    def commentDistributionByProjectWithWeekDayAndInterval(projects, date, data=None):
        """在原来的数据上面再加工，提供单独每日和星期的联合分布"""
        if data is None:
            data = commentDistribution.commentDistributionByProject(projects, date)
        print(data)

        df_fre_map = {}  # 用于统计数量
        data = data.copy(deep=True)
        data.drop(columns=['date'], inplace=True)
        groups = dict(list(data.groupby(['weekday', 'interval'])))
        for (weekday, interval), df in groups.items():
            commentCount = df.sum()
            for p in projects:
                df_fre_map[(p, weekday, interval)] = commentCount[p]

        plt.figure(21)
        for index, p in enumerate(projects):
            # 每一个项目都建立一个热力图
            # columns = ["interval"]
            columns = []
            columns.extend([str(i) for i in range(0, 24)])
            result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

            for d in range(0, 7):
                # tempDict = {"interval": i}
                tempDict = {}
                for i in range(0, 24):
                    tempDict[str(i)] = df_fre_map.get((p, d, i), 0)
                result_df = result_df.append(tempDict, ignore_index=True)
            print(result_df)
            # 在我的 notebook 里，要设置下面两行才能显示中文
            plt.rcParams['font.family'] = ['Times New Roman']
            # 如果是在 PyCharm 里，只要下面一行，上面的一行可以删除
            plt.rcParams['font.sans-serif'] = ['Times New Roman']
            result_df[list(result_df.columns)] = result_df[list(result_df.columns)].astype(float)
            plt.subplot(210 + 1 + index)
            # plt.xlabel("hour")
            # plt.ylabel("weekday")
            ax = seaborn.heatmap(result_df, annot=True, square=True, yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                                 , xticklabels=[x for x in range(0, 24)], fmt=".20g",
                                 cmap='GnBu')
            ax.set_title(p)
        plt.show()

    @staticmethod
    def commentDistributionByProjectWithWeekDayAndIntervalVersion(projects, dateList):
        """在原来的数据上面再加工，提供单独每日和星期的联合分布"""

        df_fre_map = {}  # 用于统计数量
        for project in projects:
            data = commentDistribution.commentDistributionByProjectVersion(project, dateList)
            data = data.copy(deep=True)
            data.drop(columns=['date'], inplace=True)
            groups = dict(list(data.groupby(['weekday', 'interval'])))
            for (weekday, interval), df in groups.items():
                commentCount = df.sum()
                df_fre_map[(project, weekday, interval)] = commentCount[project]

        plt.figure(21)
        for index, p in enumerate(projects):
            # 每一个项目都建立一个热力图
            # columns = ["interval"]
            columns = []
            columns.extend([str(i) for i in range(0, 24)])
            result_df = DataFrame(columns=columns)  # 用于存储最后结果的 dataframe

            for d in range(0, 7):
                # tempDict = {"interval": i}
                tempDict = {}
                for i in range(0, 24):
                    tempDict[str(i)] = df_fre_map.get((p, d, i), 0)
                result_df = result_df.append(tempDict, ignore_index=True)
            print(result_df)
            # 在我的 notebook 里，要设置下面两行才能显示中文
            plt.rcParams['font.family'] = ['Times New Roman']
            # 如果是在 PyCharm 里，只要下面一行，上面的一行可以删除
            plt.rcParams['font.sans-serif'] = ['Times New Roman']
            result_df[list(result_df.columns)] = result_df[list(result_df.columns)].astype(float)
            plt.subplot(210 + 1 + index)
            # plt.xlabel("hour")
            # plt.ylabel("weekday")
            ax = seaborn.heatmap(result_df, annot=True, square=True, yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                                 , xticklabels=[x for x in range(0, 24)], fmt=".20g",
                                 cmap='GnBu')
            ax.set_title(p)
        plt.show()


if __name__ == "__main__":
    # baseDf = commentDistribution.commentDistributionByProject(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12))

    # baseDf = commentDistribution.commentDistributionByProjectVersion('tezos', [("v1", (2020, 7, 20, 2020, 9, 1)),
    #                                                                     ("v2", (2020, 9, 1, 2020, 10, 9)),
    #                                                                     ("v3", (2020, 10, 9, 2020, 11, 14)),
    #                                                                     ("v4", (2020, 11, 14, 2020, 12, 4))])

    # """时间和周的交叉详细统计，描述看文档"""
    # """计算的df写入xlsx"""
    # fileName = "project_index.xls"
    # sheetName = "commentDistributionALL"
    # print(baseDf)
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, baseDf)
    #
    # df = commentDistribution.commentDistributionByProjectWithWeekDay(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12), baseDf)
    # df = commentDistribution.commentDistributionByProjectWithWeekDayVersion('tezos', [("v1", (2020, 7, 20, 2020, 9, 1)),
    #                                                                     ("v2", (2020, 9, 1, 2020, 10, 9)),
    #                                                                     ("v3", (2020, 10, 9, 2020, 11, 14)),
    #                                                                     ("v4", (2020, 11, 14, 2020, 12, 4))], baseDf)
    # """周的单独统计，描述看文档"""
    # """计算的df写入xlsx"""
    # fileName = "project_index.xls"
    # sheetName = "commentDistributionByWeekday"
    # print(df)
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)
    #
    # df = commentDistribution.commentDistributionByProjectWithInterval(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12), baseDf)
    # df = commentDistribution.commentDistributionByProjectWithIntervalVersion('tezos', [("v1", (2020, 7, 20, 2020, 9, 1)),
    #                                                                     ("v2", (2020, 9, 1, 2020, 10, 9)),
    #                                                                     ("v3", (2020, 10, 9, 2020, 11, 14)),
    #                                                                     ("v4", (2020, 11, 14, 2020, 12, 4))], baseDf)

    # """时间的单独统计，描述看文档"""
    # """计算的df写入xlsx"""
    # fileName = "project_index.xls"
    # sheetName = "commentDistributionByInterval"
    # print(df)
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    # """绘制项目在时间和周维度上面的评审分布的热力图，由于布局的要求，项目的列表只能选择1~2个项目，不然不好看"""
    # commentDistribution.commentDistributionByProjectWithWeekDayAndInterval(['libadblockplus-android', 'tezos'], (2019, 9, 2019, 9))

    """绘制项目在时间和周维度上面的评审分布的热力图，由于布局的要求，项目的列表只能选择1~2个项目，不然不好看"""
    commentDistribution.commentDistributionByProjectWithWeekDayAndIntervalVersion(['libadblockplus-android', 'tezos'],
                                                                                  [("v1", (2020, 7, 20, 2020, 9, 1)),
                                                                                   ("v2", (2020, 9, 1, 2020, 10, 9)),
                                                                                   ("v3", (2020, 10, 9, 2020, 11, 14)),
                                                                                   ("v4", (2020, 11, 14, 2020, 12, 4))])
