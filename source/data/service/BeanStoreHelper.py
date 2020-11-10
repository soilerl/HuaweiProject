#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/11/10 10:47
# @Author : NJU
# @Version：V 0.1
# @File : BeanStoreHelper.py
# @desc :
import os

from pandas import DataFrame

from source.data.bean.Beanbase import BeanBase
from source.utils.pandas.pandasHelper import pandasHelper


class BeanStoreHelper:
    """用于存放各种Bean对象到CSV文件中
       后面看有机会能不能用反射来做简化
    """

    @staticmethod
    def storeBeansToTSV(beanList, fileName):
        """默认是追加到文件的末尾，如果没有文件,则创建
           需要注意，beanList里面都必须是一个类型
        """
        if isinstance(beanList, list) and beanList.__len__() > 0 and isinstance(beanList[0], BeanBase):
            cols = beanList[0].getItemKeyList()
            df = DataFrame(columns=cols)
            for bean in beanList:
                if isinstance(bean, BeanBase) and type(bean) == type(beanList[0]):
                    valueMaps = bean.getValueDict()
                    df = df.append(valueMaps, ignore_index=True)

            """根据文件是否存在判读是否需要加文件头"""
            header = pandasHelper.INT_WRITE_WITH_HEADER
            if os.path.exists(fileName):
                header = pandasHelper.INT_WRITE_WITHOUT_HEADER

            pandasHelper.writeTSVFile(fileName, df,
                                      header=header,
                                      writeStyle=pandasHelper.STR_WRITE_STYLE_APPEND_NEW)
