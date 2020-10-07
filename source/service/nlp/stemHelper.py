#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/4 22:10
# @Author : NJU
# @Version：V 0.1
# @File : stemHelper.py
# @desc : 词干获取工具类


class stemHelper:
    """用于封装nlp中的stem操作
       使用SNOWball库
    """

    @staticmethod
    def stemList(wordList):
        """用于过滤单词还原到词干的状态，来减少类似的单词数

        :param wordList: 需要去除词干的单词列表
        :return: 处理完词干的结果
        """

        """基于SNOWball 的词干提取"""
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        res = []
        for word in wordList:
            stemmedWord = stemmer.stem(word)
            res.append(stemmedWord)
        return res

