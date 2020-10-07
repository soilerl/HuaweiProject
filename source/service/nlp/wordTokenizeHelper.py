#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/21 14:59
# @Author : NJU
# @Version：V 0.1
# @File : wordTokenizeHelper.py
# @desc :  分词工具类
import jieba
import jieba.posseg

import source.service.nlp.newsCorpusProcessHelper as tP

class wordTokenizeHelper:
    dic_path = "../../data/zh-dic.txt"
    dictionary = set()
    maximum = 0
    init_flag = False

    """工具类初始化"""

    def init_variable(self):
        self.dictionary = set()
        self.maximum = 0

        with open(self.dic_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)

        self.init_flag = True

    """正向最大匹配法"""

    def fmm(self, text):
        """

        :param text: 需要分词的文本
        :return: 分词结果
        """
        if not self.init_flag:
            self.init_variable()

        res = []
        length = len(text)
        index = 0
        while index < length:
            word = None
            for size in range(self.maximum, 0, -1):
                if index + size > length:
                    continue
                word = text[index: index + size]
                if word in self.dictionary:
                    res.append(word)
                    index += size
                    break
            if word is None:
                index += 1

        return res

    """逆向最大匹配法"""

    def imm(self, text):
        """

        :param text: 分词文本
        :return: 分词结果
        """
        if not self.init_flag:
            self.init_variable()

        res = []
        index = len(text)
        while index > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                word = text[index - size: index]
                if word in self.dictionary:
                    res.append(word)
                    index -= size
                    break
            if word is None:
                index -= 1

        return res[::-1]

    def bimm(self, text):
        """

        :param text: 需要分词文本
        :return: 分词结果
        """
        res1 = self.fmm(text)
        res2 = self.imm(text)

        if len(res1) < len(res2):
            return res1
        else:
            return res2

    def get_tf_from_words(words, topK=10):
        """获取单词中的高频词汇

        :param words: 文本列表
        :param topK: 选择范围
        :return: 前面的高频词汇
        """
        tf_dic = {}
        for w in words:
            tf_dic[w] = tf_dic.get(w, 0) + 1
        return sorted(tf_dic.items(), key=lambda x: x[1], reverse=True)[:topK]

    def get_stopwords(path, ecd='utf-8'):
        """从文件中获取停用词

        :param path: 停用词文件路径
        :param ecd: 文件编码
        :return: 停用词列表
        """
        with open(path, encoding=ecd) as f:
            return [line.strip() for line in f]

    def get_tf(text_path, stopwords_path, edc='utf-8', topK=10):
        """获得前k个高频的词汇，不包括停用词

        :param text_path: 文本路径
        :param stop_words_path: 停用词文本路径
        :param edc: 文本编码
        :param topK: 选择范围
        :return: 前k个高频词汇
        """
        # jieba分词
        content = tP.TextProcess.read_string(text_path)
        words = jieba.lcut(content)

        # 忽略停用词
        stopwords = wordTokenizeHelper.get_stopwords(stopwords_path, edc)
        words = [x for x in words if x not in stopwords]

        # 获取高频词汇
        return str(wordTokenizeHelper.get_tf_from_words(words, topK))
