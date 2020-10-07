#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/20 21:48
# @Author : NJU
# @Version：V 0.1
# @File : posHelper.py
# @desc :  词性标注工具类
import codecs

import jieba


class posHelper:

    @staticmethod
    def character_tagging(input_file, output_file):
        """
        :param input_file: 输入文件路径
        :param  output_file: 输入文件路径
        :return:
        """
        input_data = codecs.open(input_file, 'r', 'utf-8')
        output_data = codecs.open(output_file, 'w', 'utf-8')
        for line in input_data.readlines():
            word_list = line.strip().split()
            for word in word_list:
                if len(word) == 1:
                    output_data.write(word + "\tS\n")
                else:
                    output_data.write(word[0] + "\tB\n")
                    for w in word[1:len(word) - 1]:
                        output_data.write(w + "\tM\n")
                    output_data.write(word[len(word) - 1] + "\tE\n")
            output_data.write("\n")
        input_data.close()
        output_data.close()

    @staticmethod
    def crf_segmenter(input_file, output_file, tagger):
        """crf词性标注

        :param input_file: 输入文件路径
        :param  output_file: 输入文件路径
        :param  tagger: crf词性标注器
        :return:
        """

        input_data = codecs.open(input_file, 'r', 'utf-8')
        output_data = codecs.open(output_file, 'w', 'utf-8')
        for line in input_data.readlines():
            tagger.clear()
            for word in line.strip():
                word = word.strip()
                if word:
                    tagger.add((word + "\to\tB").encode('utf-8'))
            tagger.parse()
            size = tagger.size()
            xsize = tagger.xsize()
            for i in range(0, size):
                for j in range(0, xsize):
                    char = tagger.x(i, j).decode('utf-8')
                    tag = tagger.y2(i)
                    if tag == 'B':
                        output_data.write(' ' + char)
                    elif tag == 'M':
                        output_data.write(char)
                    elif tag == 'E':
                        output_data.write(char + ' ')
                    else:
                        output_data.write(' ' + char + ' ')
            output_data.write('\n')
        input_data.close()
        output_data.close()

    @staticmethod
    def getPartOfSpeechTaggingFromListData(sent):
        """获取给定某个句子的词性标注

        :param sent: 输入句子
        :return:
        """
        seg_list = jieba.posseg.cut(sent)
        result = []
        for w, t in seg_list:
            result.append((w, t))
        return result

