# _*_ coding: utf-8 _*_
import asyncio
from datetime import datetime

import aiomysql

from source.config.configPraser import configPraser
from source.database.SqlUtils import SqlUtils


async def getMysqlObj(loop=None):
    mysql = AsyncSqlExecuteHelper()
    pool = await mysql.initpool(loop)
    mysql.pool = pool
    return mysql


class AsyncSqlExecuteHelper:
    """使用aiomysql对数据库异步查询"""

    def __init__(self):
        self.conn = None
        self.pool = None

    async def initpool(self, loop):
        try:
            __pool = await aiomysql.create_pool(minsize=5, maxsize=10,
                                                host=configPraser.getDataBaseHost(), port=int(configPraser.getDataBasePort()),
                                                user=configPraser.getDataBaseUserName(),
                                                password=configPraser.getDataBasePassword(),
                                                db=configPraser.getDataBase(), autocommit=True, loop=loop)
            return __pool
        except Exception as e:
            print(e)

    async def getCursor(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn, cur

    # async def query(self, query, param=None):
    #     conn, cur = await self.getCursor()
    #     try:
    #         await cur.execute(query, param)
    #         return await cur.fetchall()
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         if cur:
    #             await cur.close()
    #         await self.pool.release(conn)

    async def insertValuesIntoTable(self, tableName, items, valueDict, primaryKeys=None):
        """插入语句"""

        conn, cur = await self.getCursor()

        format_table = SqlUtils.getInsertTableFormatString(tableName, items)
        format_values = SqlUtils.getInsertTableValuesString(items.__len__())

        if configPraser.getPrintMode():
            print(format_table)
            print(format_values)

        sql = SqlUtils.STR_SQL_INSERT_TABLE_UTILS.format(format_table, format_values)
        if configPraser.getPrintMode():
            print(sql)

        values = ()
        for item in items:
            values = values + (valueDict.get(item, None),)  # 元组相加

        try:
            await cur.execute(sql, values)
        except Exception as e:
            print(e)
        finally:
            if cur:
                await cur.close()
            await self.pool.release(conn)

    async def getDatabaseConnected(self):
        """返回 cursor 和 conn"""
        conn, cur = await self.getCursor()
        return conn, cur



if __name__ == '__main__':
    loop = asyncio.get_event_loop()

