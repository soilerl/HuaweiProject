import analyzeData.common as common
import csv
import datetime
import source.data.service.BeanParserHelper as bp
import source.data.bean.MergeRequest as mr

"""计算评审意见反馈时间"""


class MergeRequest:
    '''解析mermerge_request_idgeRequest.tsv需要映射的类'''
    def __init__(self, iid, created_at, merged_at, closed_at, state):
        self.iid = iid
        self.created_at = created_at
        self.merged_at = merged_at
        self.closed_at = closed_at
        self.state = state


class Notes:
    "解析mergeRequest.tsv需要映射的类"
    def __init__(self, created_at, merge_request_id):
        self.created_at = created_at
        self.merge_request_id = merge_request_id



#返回以iid为键的存放MergeRequest的字典
def getMergeRequestMap() -> dict:
    #键是iid，值是mergeRequest对象
    mergeRequestMap = {}
    arr = common.readTsvFile(common.mergeRequestTsv)
    mergeRequestList = common.getMergeRequestInstanceList(arr)
    for mergeRequest in mergeRequestList:
        iid = mergeRequest.iid
        created_at = mergeRequest.created_at
        if iid == '' or created_at == '':
            continue
        mergeRequestMap[iid] = mergeRequest
    return mergeRequestMap


def getNotesMap() -> dict:
    #字典的键是merge_request_id，值是一个存放这个mr的所有的notes的数组
    notesMap = {}
    arr = common.readTsvFile(common.notesTsv)
    notesList = common.getNotesInstanceList(arr)
    for notes in notesList:
        created_at = notes.created_at
        merge_request_id = notes.merge_request_id
        if created_at == '' or merge_request_id == '':
            continue
        if merge_request_id in notesMap:
            notesList = notesMap[merge_request_id]
            notesList.append(notes)
        else:
            notesList = []
            notesList.append(notes)
            notesMap[merge_request_id] = notesList
    return notesMap

#提取时间
def calTime(mergeRequestMap={}, notesMap={}):
    data = []
    for iid, mergeRequest in mergeRequestMap.items():
        time_list = []
        if mergeRequest.created_at != None and mergeRequest.created_at != '':
            time_list.append(tranformStrToTimestamp(mergeRequest.created_at))
        #mergeRequest的有些iid不能在notes文件中找到
        if iid not in notesMap:
            continue
        notesList = notesMap[iid]
        if mergeRequest.state == 'merged':
            time_list.extend(sortTime(mergeRequest.merged_at, notesList))
            time_list.append(tranformStrToTimestamp(mergeRequest.merged_at))
        elif mergeRequest.state == 'closed':
            time_list.extend(sortTime(mergeRequest.closed_at, notesList))
            time_list.append(tranformStrToTimestamp(mergeRequest.closed_at))
        else:
            time_list.extend(sortTime('', notesList))
        pr
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
    mergeRequestMap = getMergeRequestMap()
    notesMap = getNotesMap()
    res = calTime(mergeRequestMap, notesMap)
    for item in mergeRequestMap:
        print(item)

