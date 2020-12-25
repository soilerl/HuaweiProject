import os

import numpy
import pandas

from source.config.projectConfig import projectConfig
from source.utils.ExcelHelper import ExcelHelper

class excelDataCleaner:

    @staticmethod
    def getAvgFromSheet(filename, sheetname, projectName):
        sheet = ExcelHelper().readExcelSheet(filename, sheetname)
        print(sheet)
        # dn = pandas.read_excel(filename, sheetname, dtype="float32")
        # df = pandas.DataFrame(pandas.read_excel(filename, sheetname))
        # print(df.shape)
        nrows = sheet.nrows
        ncols = sheet.ncols
        cols = sheet.row_values(0)
        df = pandas.DataFrame(columns=cols)
        counts = [0 for i in range(0, ncols)]
        values = [0 for i in range(0, ncols)]
        for i in range(1, nrows):
            row = sheet.row_values(i)
            print(row)
            for j in range(1, ncols):
                v = row[j]
                if v != "" and not numpy.isnan(v) and v >= 0:
                    counts[j] += 1
                    values[j] += v
        print(counts)
        print(values)
        tempDict = {"project":projectName}
        for index, col in enumerate(cols):
            if index > 0:
                c = counts[index]
                v = values[index]
                if c == 0:
                    tempDict[col] = numpy.nan
                else:
                    tempDict[col] = v / c
        df = df.append(tempDict, ignore_index=True)
        print(df)
        fileName = f"project_index_{projectName}_clean.xls"
        ExcelHelper().writeDataFrameToExcel(fileName, sheetname, df)








if __name__ == "__main__":
    filename = projectConfig.getRootPath() + os.sep + "analyzeData" + os.sep + "project_index_yun.xls"
    sheetname = "commentCount"
    excelDataCleaner.getAvgFromSheet(filename, sheetname, 'yun')
