# _*_ coding: utf-8 _*_
import copy

import pandas as pd
from analyzeData import mrRateMid, timeAvgMid


class MergeRequestRateVer:
    """
    输入：一个项目的mr列表
    输出：三种rate
    类使用说明：
    1.提供初始化所用的mr列表并进行初始化
    2.调用get函数对三种rate进行获取
    ps：
    仅对一个项目进行rate计算与返回
    若要计算多个，请在外层进行循环
    """
    project = ''
    date = []

    head_label = []

    merged_rate = []  # merged的mr比例
    closed_rate = []  # closed的比例
    opened_rate = []  # opened的比例

    opened_time_avg = []
    note_time_avg = []
    ended_time_avg = []

    def __init__(self, project, date):
        """ 初始化构造函数 """
        self.project = project
        self.date = date

        """ 初始化时间列表 """
        self.set_tm(date)

        """ 初始化列表们 """
        self.init_lists(project)

    def init_lists(self, project):
        """ 初始化列表们 """
        self.merged_rate.append([project])
        self.closed_rate.append([project])
        self.opened_rate.append([project])

        self.opened_time_avg.append([project])
        self.note_time_avg.append([project])
        self.ended_time_avg.append([project])

    def set_tm(self, date):
        """ 设置时间列表 """
        self.head_label.append('project')
        for d in date:
            self.head_label.append(d[0])

    def rate_calculate1(self):
        """ 计算三种比例 """
        for d in self.date:
            mr = mrRateMid.MergeRequestRateMid([self.project], d[1])
            self.merged_rate[0].append(mr.get_df_mer()[0][1])
            self.opened_rate[0].append(mr.get_df_ope()[0][1])
            self.closed_rate[0].append(mr.get_df_clo()[0][1])

    def rate_calculate2(self):
        """ 计算三种比例 """
        for d in self.date:
            avg = timeAvgMid.TimeAvgMid([self.project], d[1])
            self.opened_time_avg[0].append(avg.get_df_ope()[0][1])
            self.note_time_avg[0].append(avg.get_df_note()[0][1])
            self.ended_time_avg[0].append(avg.get_df_end()[0][1])

    def get_df_merged_rate(self):
        return pd.DataFrame(self.merged_rate, columns=self.head_label)

    def get_df_closed_rate(self):
        return pd.DataFrame(self.closed_rate, columns=self.head_label)

    def get_df_opened_rate(self):
        return pd.DataFrame(self.opened_rate, columns=self.head_label)

    def get_df_opened_time_avg(self):
        return pd.DataFrame(self.opened_time_avg, columns=self.head_label)

    def get_df_note_time_avg(self):
        return pd.DataFrame(self.note_time_avg, columns=self.head_label)

    def get_df_ended_time_avg(self):
        return pd.DataFrame(self.ended_time_avg, columns=self.head_label)


if __name__ == '__main__':
    mrRate = MergeRequestRateVer('tezos', [("v1", (2020, 7, 20, 2020, 9, 1)),
                                            ("v2", (2020, 9, 1, 2020, 10, 9)),
                                            ("v3", (2020, 10, 9, 2020, 11, 14)),
                                            ("v4", (2020, 11, 14, 2020, 12, 4))])
    mrRate.rate_calculate2()
    df = mrRate.get_df_opened_time_avg()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrClosedRatio"
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_opened_rate()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrOpenedRatio"
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = mrRate.get_df_merged_rate()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "mrMergedRatio"
    # ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)