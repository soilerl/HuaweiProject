#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/25 23:15
# @Author : NJU
# @Version：V 0.1
# @File : htmlCorpusProcessHelper.py
# @desc :  用于处理html的文本
from bs4 import BeautifulSoup as bS


class htmlCorpusProcessHelper:

    @classmethod
    def find_tag_string(cls, text, tag, type='lxml'):
        """寻找tag对应的文本内容

        :param text: html文件
        :param tag: 目标tag
        :param type: html文件类型
        :return: tag对应的文本
        """
        bf = bS(text, type)
        res = ''
        for line in bf.find_all(tag):
            res += line.get_text()
        return res
