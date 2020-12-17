# _*_ coding: utf-8 _*_
import pandas as pd
import datetime


from analyzeData import common


class TimeAvg:
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

    ended_time_sum = {}  # 各个月的时间总长

    ended_mr_num = {}  # 各个月ended的mr个数

    ended_time_avg = []  # 各个月的平均时长

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

            self.ended_time_sum[project] = {}

            self.ended_mr_num[project] = {}

            self.ended_time_avg.append([project])

            self.set_pj_lists(project)

    def set_pj_lists(self, project):
        """ 设置列表们 """

        for time in self.time_label:
            self.merge_request_num[project][time] = 0

            self.ended_time_sum[project][time] = 0.0

            self.ended_mr_num[project][time] = 0

    def set_tm(self, date):
        """ 设置时间列表 """

        self.time_list = common.getTimeListFromTuple(date)
        self.time_label = common.getTimeLableFromTime(self.time_list)
        self.head_label = common.getTimeLableFromTime(self.time_list)
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

    def rate_calculate(self):
        """ 计算三种比例 """

        for index, project in enumerate(self.projects):
            self.set_mr(common.getMergeRequestInstances(project))

            """ 统计数量与时长 """
            for mr in self.merge_request:
                time = mr.created_at[0:7]
                head_time = self.get_datetime(mr.created_at)
                if time in self.merge_request_num[project].keys():
                    if mr.state == 'merged':
                        """ 统计数量 """
                        self.ended_mr_num[project][time] += 1
                        """ 统计时长 """
                        self.fill_time_sum(project, time, mr.merged_at, head_time)
                    elif mr.state == 'closed':
                        """ 统计数量 """
                        self.ended_mr_num[project][time] += 1
                        """ 统计时长 """
                        self.fill_time_sum(project, time, mr.closed_at, head_time)

            """ 计算每个月平均时长 """
            for i in self.merge_request_num[project].keys():
                self.ended_time_avg[index].append(int(self.ended_time_sum[project][i] /
                                                  (self.merged_mr_num[project][i] + self.closed_mr_num[project][i])))

    def fill_time_sum(self, pj, time, time_lable, head_time):
        """将时间长度填充到对应的月份中去

        pj:项目
        time:对应月份
        time_lable:结束的时间戳,用于提取结束时间
        head_time:开始时间
        """

        """ 计算结束时间 """
        tail_time = self.get_datetime(time_lable)
        """ 计算时间跨度 """
        span_time = tail_time.__sub__(head_time)
        """ 以秒结算填充至对应项目对应月份 """
        self.ended_time_sum[pj][time] += span_time.days * 86400 + span_time.seconds

    def get_datetime(self, time_lable):
        """将时间戳转化为datetime对象

        time_lable:用于转换的时间戳
        """
        return datetime.datetime.strptime(time_lable[0:19], '%Y-%m-%dT%H:%M:%S')

    def get_df_ended_time_avg(self):
        return pd.DataFrame(self.ended_time_avg, columns=self.head_label)


if __name__ == '__main__':
    ta = TimeAvg(['tezos'], (2020, 7, 2020, 9))
    df1 = ta.get_df_ended_time_avg()
    print(df1)
    print('f')
