import psycopg2
import source.utils.pgsql.StringSqlUtils as StringSqlUtils
from source.config.configPraser import configPraser

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

if __name__ == '__main__':
    connectPgsql()