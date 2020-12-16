# _*_ coding: utf-8 _*_
import os

import xlrd
import xlwt
from datetime import date

from pandas import DataFrame

from source.config.projectConfig import projectConfig
from _datetime import datetime
from xlutils import copy
from source.utils.DesensitizationHelper import DesensitizationHelper


class ExcelHelper:
    STR_KEY_REPO_NAME = 'reponame'
    STR_KEY_FILE_NAME = 'file_name'
    STR_KEY_LANGUAGE_NAME = 'language_name'
    STR_KEY_MESSAGE = 'message'
    STR_KEY_AUTHOR_EMAIL = 'author_email'
    STR_KEY_WRITTEN_ON = 'written_on'
    STR_KEY_LINE_NUMBER = 'line_number'
    STR_KEY_WORD = 'word'
    STR_KEY_FREQUENCY = 'requency'

    STR_STYLE_NORMAL = 'align: vertical center, horizontal center'
    STR_STYLE_DATE = 'YYYY/MM/DD hh:mm'
    STR_STYLE_DATA_DATE = '%Y-%m-%dT%H:%M:%SZ'

    excel_key_list = [STR_KEY_REPO_NAME, STR_KEY_FILE_NAME, STR_KEY_LANGUAGE_NAME,
                      STR_KEY_MESSAGE, STR_KEY_AUTHOR_EMAIL, STR_KEY_WRITTEN_ON,
                      STR_KEY_LINE_NUMBER]
    '''git comment数据输出抬头
    '''

    excel_key_list_split_word = [STR_KEY_WORD, STR_KEY_FREQUENCY]
    ''' 停用词输出抬头
    '''

    def initExcelFile(self, fileName, sheetName, excel_key_list=None):
        wbook = xlwt.Workbook()
        wsheet = wbook.add_sheet(sheetName)
        style = xlwt.easyxf(self.STR_STYLE_NORMAL)
        if excel_key_list is not None:
            index = 0
            for key in excel_key_list:
                wsheet.write(0, index, key, style)
                index = index + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    @staticmethod
    def getNormalStyle():
        style = xlwt.easyxf(ExcelHelper.STR_STYLE_NORMAL)
        return style

    @staticmethod
    def getDateStyle():
        style = xlwt.XFStyle()
        style.num_format_str = ExcelHelper.STR_STYLE_DATE
        return style

    def writeExcelRow(self, fileName, sheetName, startRow, startCol, dataList, style):
        ''' 覆盖  源文件必须存在 '''

        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        pos = 0
        for item in dataList:
            wsheet.write(startRow, startCol + pos, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def addSheet(self, filename, sheetName):
        rb = xlrd.open_workbook(filename, formatting_info=True)
        # make a copy of it
        from xlutils.copy import copy as xl_copy
        if sheetName not in rb.sheet_names():
            wb = xl_copy(rb)
            Sheet1 = wb.add_sheet(sheetName)
            wb.save(filename)

    def appendExcelRow(self, fileName, sheetName, dataList, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        pos = 0
        for item in dataList:
            wsheet.write(row, pos, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDataLists(self, fileName, sheetName, dataLists, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        for dataList in dataLists:
            pos = 0
            for item in dataList:
                wsheet.write(row, pos, item, style)
                pos = pos + 1
            row = row + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def appendExcelRowWithDiffStyle(self, fileName, sheetName, dataList, style):
        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)
        row = rbook.sheet_by_name(sheetName).nrows
        pos = 0
        for item in dataList:
            wsheet.write(row, pos, item, style[dataList.index(item)])
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def writeExcelCol(self, fileName, sheetName, startRow, startCol, dataList, style=None):
        ''' 覆盖  源文件必须存在 '''

        rbook = xlrd.open_workbook(fileName, formatting_info=True)
        sheetIndex = rbook.sheet_names().index(sheetName)
        if (sheetIndex == -1):  # sheet不存在就
            return

        wbook = copy.copy(rbook)
        wsheet = wbook.get_sheet(sheetIndex)

        if (style == None):
            style = self.getNormalStyle()

        pos = 0
        for item in dataList:
            wsheet.write(startRow + pos, startCol, item, style)
            pos = pos + 1
        try:
            wbook.save(fileName)
        except Exception as e:
            print(e)

    def readExcelSheet(self, fileName, sheetName, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet

    def readExcelRow(self, fileName, sheetName, startRow, startCol=0, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet.row_values(startRow)[startCol:]

    def readExcelCol(self, fileName, sheetName, startCol, startRow=0, formatting=True):
        rbook = xlrd.open_workbook(fileName, formatting_info=formatting)
        rsheet = rbook.sheet_by_name(sheetName)
        return rsheet.col_values(startCol)[startRow:]

    def desensitizationExcelCol(self, fileName, sheetName, startCol, startRow=0):
        rawData = self.readExcelCol(fileName, sheetName, startCol, startRow)
        print(rawData)
        print(rawData.__len__())
        resData = DesensitizationHelper.desensitization(rawData)
        print(resData)
        print(resData.__len__())
        self.writeExcelCol(fileName, sheetName, startRow, startCol, resData)

    def writeDataFrameToExcel(self, fileName, sheetName, dataframe):
        """写Dataframe到指定的excel
           fileName: excel的名字
           sheetName: 写入的sheetName
           dataframe: 需要写入的dataframe
        """
        if isinstance(dataframe, DataFrame):
            if not os.path.exists(path=fileName):
                self.initExcelFile(fileName, sheetName)
            else:
                self.addSheet(fileName, sheetName)

            """遍历dataframe依次加入"""
            self.appendExcelRow(fileName, sheetName, dataframe.columns, style=self.getNormalStyle())
            rows = []
            for index, row in dataframe.iterrows():
                rows.append(row)
            self.appendExcelRowWithDataLists(fileName, sheetName, rows, style=self.getNormalStyle())

if __name__ == "__main__":
    pass