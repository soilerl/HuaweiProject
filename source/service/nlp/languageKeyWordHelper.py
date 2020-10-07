#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/31 12:12
# @Author : NJU
# @Version：V 0.1
# @File : languageKeyWordHelper.py
# @desc :  用于加载不同语言的关键词


class LanguageKeyWordLanguage:

    @staticmethod
    def getJavaKeyWordList(file_path):
        """获得前java语言的关键词

        :param file_path: 文本路径
        :return: 关键词
        """
        file = open(file_path, mode='r+', encoding='utf-8')
        content = file.read()
        return content.split('\n')
