#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/8/18 22:19
# @Author : NJU
# @Version：V 0.1
# @File : newsCorpusProcessHelper.py
# @desc :  用于处理新闻文本工具类
import os


class newsCorpusProcessHelper:
    """用不同类型方式获取文本"""

    @classmethod
    def read_string(cls, path, ecd='utf-8'):
        """以string方式返回文本

        :param path: 文本路径
        :param ecd: 文件编码
        :return: 文本内容
        """
        content = ''
        with open(path, 'r', encoding=ecd, errors='ignore') as f:
            for line in f:
                line = line.strip()
                content += line
        return content

    @classmethod
    def read_list(cls, path, ecd='utf-8'):
        """以list方式返回文本

        :param path: 文本路径
        :param ecd: 文件编码
        :return: 文本内容
        """
        content = []
        with open(path, 'r', encoding=ecd, errors='ignore') as f:
            for line in f:
                line = line.strip()
                content.append(line)
        return content

    """处理文件"""

    @classmethod
    def merge_dir_files(cls, output, target, ecd='utf-8', topdown=True):
        """综合某一个目录下面的文本

        :param output: 输入文本路径
        :param target: 输出文件路径
        :param ecd: 文件编码
        :param topdown:  文件阅读顺序
        :return: None
        """
        with open(output, 'w', encoding=ecd) as f:
            for root, dirs, files in os.walk(target, topdown=topdown):
                for name in files:
                    path = os.path.join(root, name)
                    print(path)
                    with open(path, encoding=ecd) as w:
                        f.writelines(w.readlines())

    @classmethod
    def encoding_covert(cls, target, output, recd='gbk', wecd='utf-8'):
        """改变某一个文件的编码

        :param wecd: 现在的编码
        :param recd: 输出的编码
        :param output: 输入文件路径
        :param target: 输出文件路径
        :return: None
        """
        with open(output, 'w', encoding=wecd) as f:
            f.writelines(cls.read_list(target, recd))
