import os
import pandas as pd
from numpy import unicode

from source.config.projectConfig import projectConfig
from source.utils.pandas.pandasHelper import pandasHelper

if __name__ == '__main__':
    NotesDataPath = projectConfig.getNotesDataPath()
    # print(NotesDataPath)
    # NotesDataPath = r"D:\HWcoding\Githouse\外部github仓\HuaweiProject\data\file\test"
    plist = os.listdir(NotesDataPath)
    p0 = plist[0]
    prefix = str(p0)[:p0.strip().find("_", 8)]
    # content = pandasHelper.readTSVFile(NotesDataPath + os.sep + plist[0])
    # for p in plist[1:4]:
    #     ppath = NotesDataPath + os.sep + p
    #     contentnew = pandasHelper.readTSVFile(ppath)
    #     p_pre = str(p)[:p.strip().find("_", 8)]
    #     print(p)
    #     content = pd.concat([content, contentnew])
    # pandasHelper.writeTSVFile(NotesDataPath + os.sep + prefix + ".tsv", content)
    # print("finished!")

    sum = None
    for p in plist:
        if (p.find("service_") == 0):
            print(p + " is service")
            continue
        ppath = NotesDataPath + os.sep + p
        print(p)
        try:
            content = pandasHelper.readTSVFile(ppath,header=0)
        except:
            print(p+ " open with utf-8")
            content = pandasHelper.readTSVFile(ppath,header=0, encoding='utf-8')
        print(p)
        p_pre = str(p)[:p.strip().find("_", 8)]
        if (p_pre == prefix):
            if (sum is None):
                sum = content
            else:
                sum = pd.concat([sum, content])
        else:
            pandasHelper.writeTSVFile(NotesDataPath + os.sep + "service_" + prefix + ".tsv", sum)
            sum = content
            prefix = p_pre
    pandasHelper.writeTSVFile(NotesDataPath + os.sep + "service_" + prefix + ".tsv", sum)
    print("finished!")
