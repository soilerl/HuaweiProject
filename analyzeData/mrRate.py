# _*_ coding: utf-8 _*_
import pandas as pd


from analyzeData import common


class MergeRequestRate:
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

    merge_request = []  # 存放一个项目的mr列表

    notes = []

    merge_request_num = {}  # mr总个数
    merged_mr_num = {}  # merged的mr个数
    closed_mr_num = {}  # closed个数
    opened_mr_num = {}  # opened个数

    no_note_num = {}
    has_note_num = {}
    ended_mr_num = {}

    merged_rate = []  # merged的mr比例
    closed_rate = []  # closed的比例
    opened_rate = []  # opened的比例

    no_note_rate = []
    has_note_rate = []
    ended_rate = []

    default_time = '9999-99'

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

            self.merged_mr_num[project] = {}
            self.closed_mr_num[project] = {}
            self.opened_mr_num[project] = {}

            self.no_note_num[project] = {}
            self.has_note_num[project] = {}
            self.ended_mr_num[project] = {}

            self.merged_rate.append([])
            self.closed_rate.append([])
            self.opened_rate.append([])

            self.no_note_rate.append([])
            self.has_note_rate.append([])
            self.ended_rate.append([])

            self.set_pj_lists(project)

    def set_pj_lists(self, project):
        """ 设置列表们 """

        for time in self.time_label:
            self.merge_request_num[project][time] = 0
            self.merged_mr_num[project][time] = 0
            self.closed_mr_num[project][time] = 0
            self.opened_mr_num[project][time] = 0

            self.no_note_num[project][time] = 0
            self.has_note_num[project][time] = 0
            self.ended_mr_num[project][time] = 0

    def set_tm(self, date):
        """ 设置时间列表 """

        self.time_list = common.getTimeListFromTuple(date)
        self.time_label = common.getTimeLableFromTime(self.time_list)

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

            """ 对三种状态下的mr数量进行统计 """
            for mr in self.merge_request:
                time = mr.created_at[0:7]
                if time in self.merge_request_num[project].keys():
                    self.merge_request_num[project][time] += 1
                    if mr.state == 'merged':
                        self.merged_mr_num[project][time] += 1
                    elif mr.state == 'closed':
                        self.closed_mr_num[project][time] += 1
                    else:
                        self.opened_mr_num[project][time] += 1

                time_fir_nt = self.get_first_note_time(mr.iid)

                time_ended = self.get_ended_time(mr)

                if time_fir_nt == self.default_time:
                    self.fill_data(time, time_ended, self.no_note_num[project])
                else:
                    self.fill_data(time, time_fir_nt, self.no_note_num[project])
                    self.fill_data(time_fir_nt, time_ended, self.has_note_num[project])
                    self.fill_data(time_ended, self.time_label[-1], self.ended_mr_num[project])

            """ 对三种状态下的mr比例进行统计 """
            for i in self.merge_request_num[project].keys():
                sum = self.merge_request_num[project][i]

                self.merged_rate[index].append(self.merged_mr_num[project][i] / sum)
                self.closed_rate[index].append(self.closed_mr_num[project][i] / sum)
                self.opened_rate[index].append(self.opened_mr_num[project][i] / sum)

                self.no_note_rate[index].append(self.no_note_num[project][i] / sum)
                self.has_note_rate[index].append(self.has_note_num[project][i] / sum)
                self.ended_rate[index].append(self.ended_mr_num[project][i] / sum)


    def get_first_note_time(self, mr_iid):
        time = self.default_time
        for note in self.notes:
            if note.merge_request_id == mr_iid:
                time = min(note.created_at, time)
        return time[0:7]

    def get_ended_time(self, mr):
        time = self.default_time
        if mr.state == 'merged':
            time = mr.merged_at[0:7]
        elif mr.state == 'closed':
            time = mr.closed_at[0:7]
        return time

    def fill_data(self, left, right, data_list):
        start = max(left, self.time_label[0])
        end = min(right, self.time_label[-1])
        if start in self.time_label and end in self.time_label:
            for i in range(self.time_label.index(start), self.time_label.index(end)):
                data_list[self.time_label[i]] += 1

    def get_merged_rate(self):
        """ 返回merged状态的mr的比例 """
        return self.merged_rate

    def get_closed_rate(self):
        """ 返回closed状态的mr的比例 """
        return self.closed_rate

    def get_opened_rate(self):
        """ 返回opened状态的mr的比例 """
        return self.opened_rate

    def get_df_merged_rate(self):
        return pd.DataFrame(self.merged_rate, index=self.projects, columns=self.time_label)

    def get_df_closed_rate(self):
        return pd.DataFrame(self.closed_rate, index=self.projects, columns=self.time_label)

    def get_df_opened_rate(self):
        return pd.DataFrame(self.opened_rate, index=self.projects, columns=self.time_label)

    def get_df_no_note_rate(self):
        return pd.DataFrame(self.no_note_rate, index=self.projects, columns=self.time_label)

    def get_df_has_note_rate(self):
        return pd.DataFrame(self.has_note_rate, index=self.projects, columns=self.time_label)

    def get_df_ended_rate(self):
        return pd.DataFrame(self.ended_rate, index=self.projects, columns=self.time_label)


if __name__ == '__main__':
    mrRate = MergeRequestRate(['tezos'], (2020, 7, 2020, 9))
    df1 = mrRate.get_df_merged_rate()
    print(df1)
    print('f')
