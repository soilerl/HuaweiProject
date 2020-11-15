# _*_ coding: utf-8 _*_
from source.config.configPraser import configPraser
from source.data.bean.Beanbase import BeanBase
from source.data.bean.DiffRefs import DiffRefs
from source.data.bean.MergeRequest import MergeRequest
from source.data.bean.Notes import Notes
from source.data.bean.User import User
from source.database.SqlUtils import SqlUtils


class AsyncSqlHelper:

    """异步数据库操作辅助类"""

    @staticmethod
    def getInsertTableName(bean):
        """用于获得不同bean类的插入表名字"""
        if isinstance(bean, User):
            return SqlUtils.STR_TABLE_NAME_USER
        elif isinstance(bean, MergeRequest):
            return SqlUtils.STR_TABLE_NAME_MERGE_REQUEST
        elif isinstance(bean,  DiffRefs):
            return SqlUtils.STR_TABLE_NAME_DIFF_REFS
        elif isinstance(bean, Notes):
            return SqlUtils.STR_TABLE_NAME_NOTES
        else:
            return None

    @staticmethod
    async def storeBeanData(bean, mysql):
        if bean is not None and isinstance(bean, BeanBase):
            await mysql.insertValuesIntoTable(AsyncSqlHelper.getInsertTableName(bean),
                                              bean.getItemKeyList(),
                                              bean.getValueDict(),
                                              bean.getIdentifyKeys())

            print("insert success")

    @staticmethod
    async def storeBeanDateList(beans, mysql):
        """一次性存储多个bean对象 讲道理结构是被破坏的，但是可以吧所有数据库请求压缩为一次"""

        conn, cur = await  mysql.getDatabaseConnected()

        try:
            for bean in beans:
                if isinstance(bean, BeanBase):
                    tableName = AsyncSqlHelper.getInsertTableName(bean)
                    items = bean.getItemKeyList()
                    valueDict = bean.getValueDict()

                    format_table = SqlUtils.getInsertTableFormatString(tableName, items)
                    format_values = SqlUtils.getInsertTableValuesString(items.__len__())

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
        except Exception as e:
            print(e)
        finally:
            if cur:
                await cur.close()
            await mysql.pool.release(conn)

    @staticmethod
    async def queryBeanData(beans, mysql, defineItems=None):
        """一次性查询多个bean对象  define 为[[key1,key2], [key3,key4] ...]
        返回多个元组  [((),),((),())...]"""

        conn, cur = await  mysql.getDatabaseConnected()

        resultBeans = []

        try:
            pos = 0
            for bean in beans:
                if isinstance(bean, BeanBase):
                    tableName = AsyncSqlHelper.getInsertTableName(bean)
                    items = defineItems[pos]
                    if items is None:
                        items = bean.getIdentifyKeys()
                    pos += 1
                    valueDict = bean.getValueDict()

                    format_values = SqlUtils.getQueryTableConditionString(items)
                    sql = SqlUtils.STR_SQL_QUERY_TABLE_UTILS.format(tableName, format_values)

                    if configPraser.getPrintMode():
                        print(sql)

                    values = ()
                    for item in items:
                        values = values + (valueDict.get(item, None),)  # 元组相加
                    try:
                        await cur.execute(sql, values)
                        r = await cur.fetchall()
                        resultBeans.append(r)
                    except Exception as e:
                        print(e)
                        resultBeans.append(None)
        except Exception as e:
            print(e)
        finally:
            if cur:
                await cur.close()
            await mysql.pool.release(conn)

        return resultBeans

    @staticmethod
    async def updateBeanDateList(beans, mysql):
        """一次性更新多个bean对象 讲道理结构是被破坏的，但是可以吧所有数据库请求压缩为一次"""

        conn, cur = await  mysql.getDatabaseConnected()

        try:
            for bean in beans:
                if isinstance(bean, BeanBase):
                    tableName = AsyncSqlHelper.getInsertTableName(bean)
                    valueDict = bean.getValueDict()

                    format_target = SqlUtils.getUpdateTableSetString(bean.getItemKeyList())
                    format_condition = SqlUtils.getQueryTableConditionString(bean.getIdentifyKeys())
                    sql = SqlUtils.STR_SQL_UPDATE_TABLE_UTILS.format(tableName, format_target, format_condition)
                    if configPraser.getPrintMode():
                        print(sql)

                    values = ()
                    for item in bean.getItemKeyList():
                        values = values + (valueDict.get(item, None),)

                    for item in bean.getIdentifyKeys():
                        values = values + (valueDict.get(item, None),)  # 元组相加
                    try:
                        await cur.execute(sql, values)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        finally:
            if cur:
                await cur.close()
            await mysql.pool.release(conn)

    @staticmethod
    async def query(mysql, sql, values):  # 纯粹通过sql语句执行返回结果
        conn, cur = await  mysql.getDatabaseConnected()
        r = None
        try:
            try:
                await cur.execute(sql,values)
                r = await cur.fetchall()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        finally:
            if cur:
                await cur.close()
            await mysql.pool.release(conn)
        return r
