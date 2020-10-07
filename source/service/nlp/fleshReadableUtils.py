#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/9/20 22:26
# @Author : NJU
# @Version：V 0.1
# @File : fleshReadableUtils.py
# @desc :  文本易读性计算类
import math
import re

import pronouncing


class fleshReadableUtils:

    @staticmethod
    def sentenceQuestionCount(comment):
        """计算文本的疑问数量

        :param comment: 评论内容
        :return: 疑问数量
        """
        point_re = re.compile(r'\?+')
        point = point_re.findall(comment)
        print("问句数量:" + str(len(point)))
        print(point)
        return len(point)

    @staticmethod
    def CodeElement(comment):
        """计算文本的代码元素

        :param comment: 评论内容
        :return: 代码元素数量
        """
        code_re = re.compile("```[^`]*```|`[^`]+`")
        codes = re.findall(code_re, comment)
        print("codes:")
        print(codes)
        return codes

    @staticmethod
    def get_pronouncing_num(word):
        """计算单词的音节数

         :param comment: 评论内容
         :return: 单词的音节数量
         """
        try:
            pronunciating_list = pronouncing.phones_for_word(word)
            num = pronouncing.syllable_count(pronunciating_list[0])
        except Exception as e:
            print("音节计算异常，异常单词：" + word)
            return math.ceil(2)
        else:
            return num

    @staticmethod
    def get_pronouncing_nums(words):
        """计算单词的音节数总数

         :param comment: 评论内容
         :return: 单词的音节总数量
         """
        counts = 0
        for word in words:
            counts += fleshReadableUtils.get_pronouncing_num(word)
        print('音节总数：', str(counts))
        return counts