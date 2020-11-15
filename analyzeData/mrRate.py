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
    merge_request = []  # 存放一个项目的mr列表

    merge_request_num = 0  # mr总个数
    merged_mr_num = 0  # merged的mr个数
    closed_mr_num = 0  # closed个数
    opened_mr_num = 0  # opened个数

    merged_rate = 0.0  # merged的mr比例
    closed_rate = 0.0  # closed的比例
    opened_rate = 0.0  # opened的比例

    def __init__(self, merge_request):
        """ 初始化构造函数 """

        """ 初始化mr列表 """
        self.set_mr(merge_request)

        """ 计算三种比例 """
        self.rate_calculate()

    def set_mr(self, merge_request):
        """ 设置mr列表与统计mr总数 """

        """ 判断是否为列表，是的话，进行初始化 """
        if isinstance(merge_request, list):
            self.merge_request = merge_request
            self.merge_request_num = len(merge_request)

    def rate_calculate(self):
        """ 计算三种比例 """

        """ 对三种状态下的mr数量进行统计 """
        for mr in self.merge_request:
            if mr.state == 'merged':
                self.merged_mr_num += 1
            elif mr.state == 'closed':
                self.closed_mr_num += 1
            else:
                self.opened_rate += 1

        """ 对三种状态下的mr比例进行统计 """
        self.merged_rate = self.merged_mr_num / self.merge_request_num
        self.closed_rate = self.closed_mr_num / self.merge_request_num
        self.opened_rate = self.opened_mr_num / self.merge_request_num

    def get_merged_rate(self):
        """ 返回merged状态的mr的比例 """
        return self.merged_rate

    def get_closed_rate(self):
        """ 返回closed状态的mr的比例 """
        return self.closed_rate

    def get_opened_rate(self):
        """ 返回opened状态的mr的比例 """
        return self.opened_rate
