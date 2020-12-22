import analyzeData.common as common
import datetime, time
import source.data.service.BeanParserHelper as bp
import source.data.bean.MergeRequest as mr
from pandas import DataFrame
"""计算评审意见反馈时间"""




#提取时间, 返回计算每个notes的回应时间的列表和计算后的间隔时间的列表
def calTime(mergeRequestMap={}, notesMap={}) -> ([], []):
    data = []
    for iid, mergeRequest in mergeRequestMap.items():
        # mergeRequest的有些iid不能在notes文件中找到
        if iid not in notesMap:
            continue
        time_list = []
        if mergeRequest.created_at is not None and mergeRequest.created_at != '':
            time_list.append(tranformStrToTimestamp(mergeRequest.created_at))
        notesList = notesMap[iid]
        if mergeRequest.state == 'merged':
            time_list.extend(sortTime(mergeRequest.merged_at, notesList))
            time_list.append(tranformStrToTimestamp(mergeRequest.merged_at))
        elif mergeRequest.state == 'closed':
            time_list.extend(sortTime(mergeRequest.closed_at, notesList))
            time_list.append(tranformStrToTimestamp(mergeRequest.closed_at))
        else:
            time_list.extend(sortTime('', notesList))
        data.append(time_list)
    res = []
    for mr in data:
        timeDistances = []
        for index in range(len(mr)):
            if index != len(mr) - 1:
                timeDistances.append(mr[index + 1] - mr[index])
        res.append(timeDistances)
    return data, res



#将notesList中的时间进行排序
def sortTime(time='', notesList=[]) -> []:
    if time != '':
        compareTimestamp = tranformStrToTimestamp(time)
    timeList = []
    for item in notesList:
        if item.created_at == None:
            continue
        stamp = tranformStrToTimestamp(item.created_at)
        # 超过比较时间的事件被排除
        if time != '':
            if stamp > compareTimestamp:
                continue

        timeList.append(stamp)
    timeList.sort()
    return timeList


# 把字符串的时间转成时间戳
def tranformStrToTimestamp(timeStr='') -> float:
    return common.tranformStrToDateTime(timeStr).timestamp()

def classifyByTimeByProject(date, projects=[]):
    columns = ["project"]
    columns.extend(common.getTimeLableFromTime(common.getTimeListFromTuple(date)))
    replyTimeDf = DataFrame(columns=columns)
    for project in projects:
        mergeRequestMap = common.getMergeRequestMap(project)
        notesMap = common.getNotesMap(project)
        data, res = calTime(mergeRequestMap, notesMap)
        replyTimeDict = {}
        for y, m in common.getTimeListFromTuple(date):
            for index in range(len(data)):
                # 第一个数据是created_at，以created_at归入
                timeArray = time.localtime(data[index][0])
                if timeArray.tm_year == y and timeArray.tm_mon == m:
                    key = common.getTimeLableFromTime([(y, m)])[0]
                    if key in replyTimeDict.keys():
                        replyTimeDict[key].append(res[index])
                    else:
                        replyTimeDict[key] = []
                        replyTimeDict[key].append(res[index])
        resDict = {}
        for k, v in replyTimeDict.items():
            sum = 0
            avSum = 0
            for d in v:
                s = 0
                for i in d:
                    s += i
                avSum += s / len(d)
            av = avSum / len(v)
            resDict[k] = av
        resDict["project"] = project
        replyTimeDf = replyTimeDf.append(resDict, ignore_index=True)
    return replyTimeDf


if __name__ == '__main__':
    project = "tezos"

    classifyByTimeByProject(["tezos"], (2020, 7, 2020, 9))
    # for i in res:
    #     print(res)
