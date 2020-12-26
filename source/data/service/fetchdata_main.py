from source.data.service.AsyncApiHelper import AsyncApiHelper
from source.data.service.AsyncProjectAllDataFetcher import AsyncProjectAllDataFetcher

from source.utils.StringKeyUtils import StringKeyUtils
import pandas as pd

if __name__ == '__main__':
    data = pd.read_excel(r"C:\Users\z50016351\Desktop\新项目代码仓库地址\PPS7个服务1207.xlsx", sheet_name="de_duplicates")
    prefix = "open_platform"
    data = data[['spname', 'git仓地址PipelineCheck', 'pid']]
    list = list(data)
    for d in data.itertuples():
        spname = d.__getattribute__('spname')
        url = d.__getattribute__('git仓地址PipelineCheck')
        pid = d.__getattribute__('pid')
        # spname = str(sname).strip()+'-'+str(ppname).strip()
        AsyncProjectAllDataFetcher.getProjectAllMergeRequestNum(pid)
        mr_mum = AsyncApiHelper.mr_num
        p = (pid, prefix, spname, mr_mum - 1, mr_mum)
        #     开始获取数据
        print(f"begin:PPS:|{p[2]}|{p[3]}|{p[4]}|----------Fetch begin!-------------")
        AsyncProjectAllDataFetcher.getDataForRepository(p[0], p[1], p[2], p[3], p[4])
        print(f"PPS: {p[0]}| {p[1]}|{p[2]}|----------Fetch Finish!-------------")

# pps_list = StringKeyUtils.pps_list
# for p in pps_list:
#     prefix = "open_platform"
#     pid = pid
#     mr_mum= AsyncProjectAllDataFetcher.getProjectAllMergeRequestNum(id, prefix, p)
# print(AsyncApiHelper.mr_num)
