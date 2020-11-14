import analyzeData.common as common
import csv
import datetime
import source.data.service.BeanParserHelper as bp
import source.data.bean.MergeRequest as mr

"""计算评审意见反馈时间"""




#提取时间
def calTime(mergeRequestMap={}, notesMap={}) -> []:
    data = []
    for iid, mergeRequest in mergeRequestMap.items():
        # mergeRequest的有些iid不能在notes文件中找到
        if iid not in notesMap:
            continue
        time_list = []
        if mergeRequest.created_at != None and mergeRequest.created_at != '':
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
    return data



#将notesList中的时间进行排序
def sortTime(time='', notesList=[]) -> []:
    if time != '':
        compareTimestamp = tranformStrToTimestamp(time)
    timeList = []
    for item in notesList:
        if item.created_at == None:
            continue
        stamp = tranformStrToTimestamp(item.created_at)
        #超过比较时间的事件被排除
        if time != '':
            if stamp > compareTimestamp:
                continue

        timeList.append(stamp)
    timeList.sort()
    return timeList

#把字符串的时间转成时间戳
def tranformStrToTimestamp(timeStr='') -> float:
    try:
        if '.' in timeStr:
            timeStr = timeStr.split(".")[0]
        else:
            timeStr = timeStr[:-1]
        timeArray = datetime.datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
    except:
        print(timeStr)
    return timeArray.timestamp()

if __name__ == '__main__':
    mergeRequestMap = common.getMergeRequestMap()
    notesMap = common.getNotesMap()
    res = calTime(mergeRequestMap, notesMap)
    for i in res:
        print(res)
