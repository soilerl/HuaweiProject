# _*_ coding: utf-8 _*_
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
    # 获取项目的所有信息 主题信息采用异步获取

    @staticmethod
    def getDataForRepository(repo_id, owner, repo, limit, start):
        """指定目标owner/repo 获取start到  start - limit编号的pull-request相关评审信息"""

        """获取repo信息  这里的owner就是gitlab中的namespace"""
        AsyncApiHelper.setRepo(owner, repo)
        AsyncApiHelper.setRepoId(repo_id)
        t1 = datetime.now()

        statistic = statisticsHelper()
        statistic.startTime = t1

        """异步多协程爬虫爬取pull-request信息"""
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
        """准备工作"""
        semaphore = asyncio.Semaphore(configPraser.getSemaphore())  # 对速度做出限制
        """多协程"""
        tasks = [asyncio.ensure_future(AsyncApiHelper.downloadInformation(pull_number, semaphore, statistic))
                 for pull_number in range(start, max(start - limit, 0), -1)]
        await asyncio.wait(tasks)


if __name__ == '__main__':
    """1. 获取基础数据"""
    # 格式说明: 项目编号repo_id, namespace, name, 需要爬取的pr数量, pr的结束编号
    projects = [(3836952, "tezos", "tezos", 100, 2093)]
    for p in projects:
        AsyncProjectAllDataFetcher.getDataForRepository(p[0], p[1], p[2], p[3], p[4])

