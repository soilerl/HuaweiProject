# coding=gbk
import asyncio
import json
import os
import time
from datetime import datetime
import random
import numpy as np
import math


from source.config.configPraser import configPraser
from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.database.AsyncSqlExecuteHelper import getMysqlObj
from source.utils.statisticsHelper import statisticsHelper


class AsyncProjectAllDataFetcher:
    # ��ȡ��Ŀ��������Ϣ ������Ϣ�����첽��ȡ

    @staticmethod
    def getDataForRepository(repo_id, owner, repo, limit, start):
        """ָ��Ŀ��owner/repo ��ȡstart��  start - limit��ŵ�pull-request���������Ϣ"""

        """��ȡrepo��Ϣ  �����owner����gitlab�е�namespace"""
        AsyncApiHelper.setRepo(owner, repo)
        AsyncApiHelper.setRepoId(repo_id)
        t1 = datetime.now()

        statistic = statisticsHelper()
        statistic.startTime = t1

        """�첽��Э��������ȡpull-request��Ϣ"""
        loop = asyncio.get_event_loop()
        task = [asyncio.ensure_future(AsyncProjectAllDataFetcher.preProcess(loop, limit, start, statistic))]
        tasks = asyncio.gather(*task)
        loop.run_until_complete(tasks)

        print("useful pull request:", statistic.usefulRequestNumber,
              " useful review:", statistic.usefulReviewNumber,
              " useful review comment:", statistic.usefulReviewCommentNumber,
              " useful issue comment:", statistic.usefulIssueCommentNumber,
              " useful commit:", statistic.usefulCommitNumber,
              " cost time:", datetime.now() - statistic.startTime)

    @staticmethod
    async def preProcess(loop, limit, start, statistic):
        """׼������"""
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # ���ٶ���������
        """��Э��"""
        tasks = [asyncio.ensure_future(AsyncApiHelper.downloadInformation(pull_number, semaphore, statistic))
                 for pull_number in range(start, max(start - limit, 0), -1)]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    """1. ��ȡ��������"""
    # ��ʽ˵��: ��Ŀ���repo_id, namespace, name, ��Ҫ��ȡ��pr����, pr�Ľ������
    projects = [(3836952, "tezos", "tezos", 300, 2000)]
    for p in projects:
        AsyncProjectAllDataFetcher.getDataForRepository(p[0], p[1], p[2], p[3], p[4])

