# _*_ coding: utf-8 _*_
from source.config.configPraser import configPraser
from source.data.bean.Beanbase import BeanBase


class BeanParserHelper:
    """bean 类的一些其他parser方式"""

    @staticmethod
    def getBeansFromTuple(beanClass, columns, dataTuple):
        result = []
        if configPraser.getPrintMode():
            print(columns)
        if isinstance(beanClass, BeanBase):
            """采用反射机制实例化对象"""
            obj = beanClass.__class__()
            itemList = obj.getItemKeyList()
            for index, item in enumerate(itemList):
                value = BeanParserHelper.findItemInArray(item, columns, dataTuple)
                if value is not None:
                    setattr(obj, item, value)
            result.append(obj)
        if configPraser.getPrintMode():
            print(result.__len__())
        return result

    @staticmethod
    def findItemInArray(item, columns, array):
        index = -1
        try:
            index = columns.index(item)
        except Exception as e:
            pass
        if index == -1:
            return None
        return array[index]

