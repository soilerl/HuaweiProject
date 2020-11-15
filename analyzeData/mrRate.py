class MergeRequestRate:
    """
    ���룺һ����Ŀ��mr�б�
    ���������rate

    ��ʹ��˵����
    1.�ṩ��ʼ�����õ�mr�б����г�ʼ��
    2.����get����������rate���л�ȡ

    ps��
    ����һ����Ŀ����rate�����뷵��
    ��Ҫ������������������ѭ��
    """
    merge_request = []  # ���һ����Ŀ��mr�б�

    merge_request_num = 0  # mr�ܸ���
    merged_mr_num = 0  # merged��mr����
    closed_mr_num = 0  # closed����
    opened_mr_num = 0  # opened����

    merged_rate = 0.0  # merged��mr����
    closed_rate = 0.0  # closed�ı���
    opened_rate = 0.0  # opened�ı���

    def __init__(self, merge_request):
        """ ��ʼ�����캯�� """

        """ ��ʼ��mr�б� """
        self.set_mr(merge_request)

        """ �������ֱ��� """
        self.rate_calculate()

    def set_mr(self, merge_request):
        """ ����mr�б���ͳ��mr���� """

        """ �ж��Ƿ�Ϊ�б��ǵĻ������г�ʼ�� """
        if isinstance(merge_request, list):
            self.merge_request = merge_request
            self.merge_request_num = len(merge_request)

    def rate_calculate(self):
        """ �������ֱ��� """

        """ ������״̬�µ�mr��������ͳ�� """
        for mr in self.merge_request:
            if mr.state == 'merged':
                self.merged_mr_num += 1
            elif mr.state == 'closed':
                self.closed_mr_num += 1
            else:
                self.opened_rate += 1

        """ ������״̬�µ�mr��������ͳ�� """
        self.merged_rate = self.merged_mr_num / self.merge_request_num
        self.closed_rate = self.closed_mr_num / self.merge_request_num
        self.opened_rate = self.opened_mr_num / self.merge_request_num

    def get_merged_rate(self):
        """ ����merged״̬��mr�ı��� """
        return self.merged_rate

    def get_closed_rate(self):
        """ ����closed״̬��mr�ı��� """
        return self.closed_rate

    def get_opened_rate(self):
        """ ����opened״̬��mr�ı��� """
        return self.opened_rate
