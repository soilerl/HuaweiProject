#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/15 22:31
# @Author : NJU
# @Version：V 0.1
# @File : ChangeTriggerUtils.py
# @desc :
from source.utils.pandas.pandasHelper import pandasHelper
import matplotlib.pyplot as plt


class ChangeTriggerUtils:
    """用于分析处理
    评审触发代码变更"""

    @staticmethod
    def change_trigger_analyser(project):
        df_review = pandasHelper.readTSVFile(f"{project}_comment.cvs")
        df_review.columns = ["merge_request_id", "reviewer", "id", "change_trigger", "body"]
        df_review.drop_duplicates(inplace=True)
        print(df_review.shape)

        x = range(-2, 11)
        y = []
        for i in x:
            y.append(df_review.loc[df_review['change_trigger'] == i].shape[0])
        plt.bar(x=x, height=y)
        plt.title(f'review comment({project})')
        for a, b in zip(x, y):
            plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=11)

        print("review comment useful:", df_review.shape[0] - df_review.loc[df_review['change_trigger'] == -1].shape[0])
        plt.show()


if __name__ == "__main__":
    ChangeTriggerUtils.change_trigger_analyser("tezos")
