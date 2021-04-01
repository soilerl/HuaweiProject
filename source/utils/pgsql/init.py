import psycopg2
import source.utils.pgsql.StringSqlUtils as StringSqlUtils
from source.config.configPraser import configPraser
from datetime import date,datetime,timezone
import time

def connectPgsql():
    conn = psycopg2.connect(database=configPraser.getPgsqlDatabaseName(),
                            user=configPraser.getPgsqlUser(),
                            password=configPraser.getPgsqlPassword(),
                            host=configPraser.getPgsqlHost(),
                            port=configPraser.getPgsqlPort()
                            )
    cur = conn.cursor()
    return cur, conn

#获取所有的指标数据
def getAllIndex() -> []:
    urlList = []
    cur, conn = connectPgsql()
    cur.execute(StringSqlUtils.getAllUrls)
    rows = cur.fetchall()
    for row in rows:
        urlList.append(row)
    conn.close()
    return urlList

#更新指标数据，如果没有则添加
def updateData(url, data):
    cur, conn = connectPgsql()
    cur.execute(StringSqlUtils.getIndexByUrl.format(url=url))
    rows = cur.fetchall()

    if rows == None or len(rows) == 0:
        cur.execute(StringSqlUtils.insertIndex.format(url=url, data=data))
    else:
        cur.execute(StringSqlUtils.updateIndex.format(url=url, data=data))
    conn.commit()
    conn.close()

def writeWeekDayDataToDatabase(projectName, calTimeRange, createdAt, meteicName, projectId, weekDayMetric={}):
    cur, conn = connectPgsql()
    cur.execute(StringSqlUtils.updateWeekDayMetric.format(sunday=weekDayMetric['0'], monday=weekDayMetric['1'],
                                                          tuesday=weekDayMetric['2'], wednesday=weekDayMetric['3'],
                                                          thursday=weekDayMetric['4'], friday=weekDayMetric['5'],
                                                          saturday=weekDayMetric['6'], project_name=projectName,
                                                          cal_time_range=calTimeRange, created_at=createdAt,
                                                          metric_name=meteicName, project_id=projectId
                                                          ))
    conn.commit()
    conn.close()

def writeDayPerHourDataToDatabase(projectName, calTimeRange, createdAt, metricName, projectId, dayPerHourDic={}):
    cur, conn = connectPgsql()
    cur.execute(StringSqlUtils.updateDayPerHourMetric.format(dayPerHourDic['0'], dayPerHourDic['1'], dayPerHourDic['2'],
                                                             dayPerHourDic['3'], dayPerHourDic['4'], dayPerHourDic['5'],
                                                             dayPerHourDic['6'], dayPerHourDic['7'], dayPerHourDic['8'],
                                                             dayPerHourDic['9'], dayPerHourDic['10'], dayPerHourDic['11'],
                                                             dayPerHourDic['12'], dayPerHourDic['13'], dayPerHourDic['14'],
                                                             dayPerHourDic['15'], dayPerHourDic['16'], dayPerHourDic['17'],
                                                             dayPerHourDic['18'], dayPerHourDic['19'], dayPerHourDic['20'],
                                                             dayPerHourDic['21'], dayPerHourDic['22'], dayPerHourDic['23'],
                                                             projectName, calTimeRange, metricName, projectId, createdAt
                                                             ))
    conn.commit()
    conn.close()

def writeMonthDataToDatabase(projectName, calTimeRange, createdAt, meteicName, projectId, metric_time, metric_data):
    cur, conn = connectPgsql()
    cur.execute(StringSqlUtils.updateMonthMetric.format(projectName, meteicName, calTimeRange, createdAt, metric_time,
                                                        metric_data, projectId))
    conn.commit()
    conn.close()

def testDate():
    cur, conn = connectPgsql()
    cur.execute("""INSERT INTO public.test(
	name, age, created_at)
	VALUES ('s', 1, '{created_at}')""".format(created_at=datetime.now(tz=timezone.utc)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    testDate()