#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/10/15 22:31
# @Author : NJU
# @Version：V 0.1
# @File : ChangeTriggerUtils.py
# @desc :
import time

import pandas
from pandas import DataFrame

from source.utils.StringKeyUtils import StringKeyUtils
from source.utils.pandas.pandasHelper import pandasHelper
import matplotlib.pyplot as plt


class ChangeTriggerUtils:
    """用于分析处理
    评审触发代码变更"""

    @staticmethod
    def change_trigger_analyser(project):
        df_review = pandasHelper.readTSVFile(f"{project}_comment_1.cvs")
        df_review.columns = ["merge_request_id", "reviewer", "id", "change_trigger", "body"]
        df_review.drop_duplicates(subset=['id'], inplace=True, keep="last")
        df_review.sort_values(by='merge_request_id', ascending=False, inplace=True)
        print(df_review.shape)

        df_mr = pandasHelper.readTSVFile(f"mergeRequest.csv", sep=StringKeyUtils.STR_SPLIT_SEP_CSV)
        df_mr.columns = ["id", "number", "state", "merged_at", "created_at", "1", "2", "3", "4"]

        """日期修补"""
        for index, row in df_mr.iterrows():
            if row["created_at"] is None:
                row["created_at"] = row["merged_at"]

        df_mr = df_mr[["number", "created_at"]].copy(deep=True)
        df_mr["number"] = df_mr["number"].apply(lambda x: int(x))
        df_mr.drop_duplicates(subset=['number'], inplace=True)

        print(df_mr.shape)

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


        data = pandas.merge(left=df_review, right=df_mr, left_on="merge_request_id", right_on="number")
        data['label'] = data["created_at"].apply(lambda x: (time.strptime(x, "%Y-%m-%dT%H:%M:%SZ")))
        data['label_y'] = data['label'].apply(lambda x: x.tm_year)
        data['label_m'] = data['label'].apply(lambda x: x.tm_mon)

        data = data.loc[data["change_trigger"] != -2].copy(deep=True)


        pandasHelper.writeTSVFile("comment.csv", df_review)

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
                tempDict = {"reviewer":reviewer}
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
    ChangeTriggerUtils.change_trigger_analyser("tezos")
