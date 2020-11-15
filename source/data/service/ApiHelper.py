# _*_ coding: utf-8 _*_
import random

import requests
import sys
import json
import io
import time

import os

import urllib3
from urllib3.exceptions import InsecureRequestWarning

from source.config import projectConfig
from source.config import configPraser
from source.data.service.ProxyHelper import ProxyHelper
from source.utils.StringKeyUtils import StringKeyUtils
from _datetime import datetime
from math import ceil


class ApiHelper:

    """
    同步方式请求 api接口类
    """

    def __init__(self, owner, repo):  # 设置对应的仓库和所属
        self.owner = owner
        self.repo = repo
        self.isUseAuthorization = False
        self.isUseProxyPool = False

    def setOwner(self, owner):
        self.owner = owner

    def setRepo(self, repo):
        self.repo = repo

    def setAuthorization(self, isUseAuthorization):
        self.isUseAuthorization = isUseAuthorization

    def setUseProxyPool(self, isUseProxyPool):
        self.isUseProxyPool = isUseProxyPool

    def getProxy(self):
        if self.isUseProxyPool:
            proxy = ProxyHelper.getSingleProxy()
            if configPraser.configPraser.getPrintMode():
                print(proxy)
            if proxy is not None:
                return {StringKeyUtils.STR_PROXY_HTTP: StringKeyUtils.STR_PROXY_HTTP_FORMAT.format(proxy)}
        return None

    def getAuthorizationHeaders(self, header):
        if header is not None and isinstance(header, dict):
            if self.isUseAuthorization:
                if configPraser.configPraser.getAuthorizationToken():
                    header[StringKeyUtils.STR_HEADER_AUTHORIZAITON] = (StringKeyUtils.STR_HEADER_TOKEN
                                                             + configPraser.configPraser.getAuthorizationToken())

        return header

    def getUserAgentHeaders(self, header):
        if header is not None and isinstance(header, dict):
            # header[self.STR_HEADER_USER_AGENT] = self.STR_HEADER_USER_AGENT_SET
            header[StringKeyUtils.STR_HEADER_USER_AGENT] = random.choice(StringKeyUtils.USER_AGENTS)
        return header

    def getMediaTypeHeaders(self, header):
        if header is not None and isinstance(header, dict):
            header[StringKeyUtils.STR_HEADER_ACCEPT] = StringKeyUtils.STR_HEADER_MEDIA_TYPE

        return header

    def printCommon(self, r):
        if configPraser.configPraser.getPrintMode():
            if isinstance(r, requests.models.Response):
                print(type(r))
                print(r.json())
                print(r.text.encode(encoding='utf_8', errors='strict'))
                print(r.headers)
                print("status:", r.status_code.__str__())
                print("remaining:", r.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
                print("rateLimit:", r.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_RESET))

    def judgeLimit(self, r):
        if isinstance(r, requests.models.Response):
            remaining = int(r.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_REMIAN))
            rateLimit = int(r.headers.get(StringKeyUtils.STR_HEADER_RATE_LIMIT_RESET))
            if remaining < StringKeyUtils.RATE_LIMIT:
                print("start sleep:", ceil(rateLimit - datetime.now().timestamp() + 1))
                time.sleep(ceil(rateLimit - datetime.now().timestamp() + 1))
                print("sleep end")

if __name__ == "__main__":
    helper = ApiHelper('rails', 'rails')
    helper.setAuthorization(True)
    helper.setUseProxyPool(True)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # print(helper.getReviewForPullRequest(38211))
    # helper.getPullRequestsForPorject(state = ApiHelper.STR_PARM_ALL)
    #     print("total:" + helper.getTotalPullRequestNumberForProject().__str__())
    #     print(helper.getCommentsForReview(38211,341374357))
    #     print(helper.getCommentsForPullRequest(38211))
    #     print(helper.getCommentsForPullRequest(38211))
    # print(helper.getMaxSolvedPullRequestNumberForProject())
    # print(helper.getLanguageForProject())
    # print(helper.getInformationForProject().getItemKeyListWithType())
    # print(helper.getInformationForUser('jonathanhefner').getItemKeyListWithType())
    # print(helper.getTotalPullRequestNumberForProject())
    # print(Branch.getItemKeyListWithType())
    # print(helper.getInformationForPullRequest(38383).getValueDict())
    # print(Review.getItemKeyListWithType())
    # print(helper.getInformationForReview(38211, 341373994).getValueDict())
    # print(helper.getInformationForReviewWithPullRequest(38211))
    # print(helper.getInformationForReviewCommentWithPullRequest(38539))
    # print(helper.getInformationForIssueCommentWithIssue(38529))
    # print(CommitRelation.getItemKeyList())
    # print(CommitRelation().getValueDict())
    # print(helper.getInformationForCommit('b4256cea5d812660f28ca148835afcf273376c8e').parents[0].getValueDict())
    # print(helper.getInformationForCommitWithPullRequest(38449))
    # print(helper.getInformationForCommitCommentsWithCommit('2e74177d0b61f872b773285471ff9025f0eaa96c'))
