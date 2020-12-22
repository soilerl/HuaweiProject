# _*_ coding: utf-8 _*_
import pandas
import pandas as pd
import datetime

from pandas import DataFrame

from analyzeData import common
from source.utils.ExcelHelper import ExcelHelper


class TimeSpan:
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
    projects = []
    time_list = []
    time_label = []
    head_label = []

    merge_request = []  # 存放一个项目的mr列表

    notes = []  # 存放一个项目的notes

    merge_request_num = {}  # mr总个数

    no_note_num = {}  # 提交但未有note的数量
    has_note_num = {}  # 有note但未完结的数量
    ended_mr_num = {}  # 结束之后的数量

    no_note_rate = []  # 提交但未有note的比例
    has_note_rate = []  # 有note但未完结的比例
    ended_rate = []  # 结束之后的比例

    default_time = '9999-99-99'

    def __init__(self, projects, date):
        """ 初始化构造函数 """

        """ 初始化项目列表 """
        self.set_pj(projects)

        """ 初始化时间列表 """
        self.set_tm(date)

        """ 初始化列表们 """
        self.init_lists()

        """ 计算三种比例 """
        self.rate_calculate()

    def init_lists(self):
        """ 初始化列表们 """

        for project in self.projects:
            self.merge_request_num[project] = {}

            self.no_note_num[project] = {}
            self.has_note_num[project] = {}
            self.ended_mr_num[project] = {}

            self.no_note_rate.append([project])
            self.has_note_rate.append([project])
            self.ended_rate.append([project])

            self.set_pj_lists(project)

    def set_pj_lists(self, project):
        """ 设置列表们 """

        for time in self.time_label:
            self.merge_request_num[project][time] = 0

            self.no_note_num[project][time] = 0
            self.has_note_num[project][time] = 0
            self.ended_mr_num[project][time] = 0

    def set_tm(self, date):
        """ 设置时间列表 """

        """粒度换成了day"""
        self.time_list = common.getDayListFromTuple(date)
        self.time_label = common.getDayLabelFromTime(self.time_list)
        self.head_label = common.getDayLabelFromTime(self.time_list)
        self.head_label.insert(0, 'project')

    def set_pj(self, projects):
        """ 设置project列表 """

        if isinstance(projects, list):
            self.projects = projects

    def set_mr(self, merge_request):
        """ 设置mr列表与统计mr总数 """

        """ 判断是否为列表，是的话，进行初始化 """
        if isinstance(merge_request, list):
            self.merge_request = merge_request
            # self.merge_request_num = len(merge_request)

    def set_nt(self, notes):

        if isinstance(notes, list):
            self.notes = notes

    def rate_calculate(self):
        """ 计算三种比例 """

        for index, project in enumerate(self.projects):
            self.set_mr(common.getMergeRequestInstances(project))

            self.set_nt(common.getNotesInstances(project))

            """ 对三种时间戳进行获取 """
            for mr in self.merge_request:
                """ 获取created """
                time = mr.created_at[0:10]
                """ 获取第一个note的时间 """
                time_fir_nt = self.get_first_note_time(mr.iid, mr.closed_at)
                """ 获取ended """
                time_ended = self.get_ended_time(mr)

                """ 对数量进行统计 """
                if time_fir_nt == self.default_time:
                    """ 不存在第一个note的情况；此时分为created到ended，ended到大时间边界 """
                    self.fill_data(time, time_ended, self.no_note_num[project])
                    self.fill_data(time_ended, self.time_label[-1], self.ended_mr_num[project])

                else:
                    """ 存在第一个note的情况；此时分为created到first note，first note到ended，ended到大时间边界 """
                    self.fill_data(time, time_fir_nt, self.no_note_num[project])
                    self.fill_data(time_fir_nt, time_ended, self.has_note_num[project])
                    self.fill_data(time_ended, self.time_label[-1], self.ended_mr_num[project])

            """ 对三种状态下的比例进行统计 """
            for i in self.merge_request_num[project].keys():
                sum = len(self.merge_request)

                self.no_note_rate[index].append(self.no_note_num[project][i])
                self.has_note_rate[index].append(self.has_note_num[project][i])
                self.ended_rate[index].append(self.ended_mr_num[project][i])


    def get_first_note_time(self, mr_iid, endtime=None):
        """获取此mr的第一个note的时间

        mr_iid:要获取的那个mr
        """
        time = self.default_time
        for note in self.notes:
            if note.merge_request_id == mr_iid:
                time = min(note.created_at, time)
        return time[0:10]

    def get_ended_time(self, mr):
        """获取此mr的ended时间

        mr:要获取的那个mr
        """
        time = self.default_time
        if mr.state == 'merged':
            time = mr.merged_at[0:10]
        elif mr.state == 'closed':
            time = mr.closed_at[0:10]
        return time

    def fill_data(self, left, right, data_list):
        """填充计数器

        left:左边界
        right:右边界
        data_list:要填充的填充器
        """
        """ 与大时间范围的左边界比较得出真正的左边界 """
        start = max(left, self.time_label[0])
        """ 与大时间范围的右边界比较得出真正的右边界 """
        end = min(right, self.time_label[-1])
        """ 边界内月份遍历填充 """
        if start in self.time_label and end in self.time_label:
            for i in range(self.time_label.index(start), self.time_label.index(end)):
                data_list[self.time_label[i]] += 1

    def get_df_no_note_count(self):
        return pd.DataFrame(self.no_note_rate, columns=self.head_label)

    def get_df_has_note_count(self):
        return pd.DataFrame(self.has_note_rate, columns=self.head_label)

    def get_df_ended_count(self):
        return pd.DataFrame(self.ended_rate, columns=self.head_label)


if __name__ == '__main__':
    ts = TimeSpan(['tezos', 'libadblockplus-android'], (2019, 9, 2020, 12))
    df = ts.get_df_no_note_count()
    """计算的df写入xlsx"""
    fileName = "project_index1.xls"
    sheetName = "df_no_note_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    df['date'] = columns
    df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = ts.get_df_has_note_count()
    """计算的df写入xlsx"""
    fileName = "project_index1.xls"
    sheetName = "df_has_note_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    df['date'] = columns
    df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

    df = ts.get_df_ended_count()
    """计算的df写入xlsx"""
    fileName = "project_index.xls"
    sheetName = "df_ended_count"
    columns = list(df.columns)
    df = pandas.DataFrame(df.values.T, columns=df.index)
    df['date'] = columns
    df = df[["date", 0, 1]]
    ExcelHelper().writeDataFrameToExcel(fileName, sheetName, df)

