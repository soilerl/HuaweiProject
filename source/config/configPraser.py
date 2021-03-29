# _*_ coding: utf-8 _*_
import os
import random

from source.config.projectConfig import projectConfig
import configparser


class configPraser:  #用于解析config.ini文件

    STR_TOKEN = 'token'
    STR_AUTHORIZATION = 'authorization'
    STR_PRIVATE_TOKEN = 'privateToken'
    STR_MONGODB = 'mongoDB'
    STR_DEBUG = 'debug'
    STR_PROJECT = 'project'
    STR_NETWORK = 'network'
    STR_RECOMMEND = 'recommend'
    STR_NLP = 'nlp'

    STR_USERNAME = 'username'
    STR_PASSWORD = 'password'
    STR_PRINT = 'print'
    STR_TRUE = 'True'
    STR_RETRY = 'retry'
    STR_OWNER = 'owner'
    STR_REPO = 'repo'
    STR_LIMIT = 'limit'
    STR_PROXY = 'proxy'
    STR_START = 'start'
    STR_TIMEOUT = 'timeout'
    STR_SEMAPHORE = 'semaphore'
    STR_API = 'api'
    STR_TOPK = 'topk'
    STR_TEST_NUMBER = 'testNumber'
    STR_REVIEWER_NUMBER = 'reviewerNumber'
    STR_FPS_REMOVE_AUTHOR = 'FPSRemoveAuthor'
    STR_FPS_CTYPES = 'FPSCtypes'
    STR_COMMIT_FETCH_LOOP = 'commitFetchLoop'
    STR_CHANGE_TRIGGER_BY_LINE = 'changeTriggerByLine'
    STR_JVM_PATH = 'JVMPath'
    STR_STANFORD_MODEL_PATH = 'stanfordModelPath'
    STR_TIME_RANGE = 'timeRange'
    STR_INDEX = 'index'
    STR_URL = 'url'
    STR_START_YEAR = 'startYear'
    STR_START_MONTH = 'startMonth'
    STR_END_YEAR = 'endYear'
    STR_END_MONTH = 'endMonth'
    STR_UPDATE_TIME = 'updateTime'


    STR_HOST = 'host'
    STR_PORT = 'port'
    STR_DB_NAME = 'databaseName'


    cacheDict = {}  # 用于缓存的字典，防止多次访问拖慢速度

    @staticmethod
    def getAuthorizationToken():
        temp = configPraser.cacheDict.get((configPraser.STR_AUTHORIZATION, configPraser.STR_TOKEN), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            tokenList = cp.get(configPraser.STR_AUTHORIZATION, configPraser.STR_TOKEN).split(',')
            configPraser.cacheDict[(configPraser.STR_AUTHORIZATION, configPraser.STR_TOKEN)] = tokenList
            return tokenList[random.randint(0, tokenList.__len__() - 1)]
        else:
            return temp[random.randint(0, temp.__len__() - 1)]

    @staticmethod
    def getPrivateToken():
        temp = configPraser.cacheDict.get((configPraser.STR_AUTHORIZATION, configPraser.STR_PRIVATE_TOKEN), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            tokenList = cp.get(configPraser.STR_AUTHORIZATION, configPraser.STR_PRIVATE_TOKEN).split(',')
            configPraser.cacheDict[(configPraser.STR_AUTHORIZATION, configPraser.STR_PRIVATE_TOKEN)] = tokenList
            return tokenList[random.randint(0, tokenList.__len__() - 1)]
        else:
            return temp[random.randint(0, temp.__len__() - 1)]


    @staticmethod
    def getPrintMode():
        temp = configPraser.cacheDict.get((configPraser.STR_DEBUG, configPraser.STR_PRINT), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = cp.get(configPraser.STR_DEBUG, configPraser.STR_PRINT) == configPraser.STR_TRUE
            configPraser.cacheDict[(configPraser.STR_DEBUG, configPraser.STR_PRINT)] = res
            return res
        else:
            return temp

    @staticmethod
    def getProxy():
        temp = configPraser.cacheDict.get((configPraser.STR_NETWORK, configPraser.STR_PROXY), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = cp.get(configPraser.STR_NETWORK, configPraser.STR_PROXY) == configPraser.STR_TRUE
            configPraser.cacheDict[(configPraser.STR_NETWORK, configPraser.STR_PROXY)] = res
            return res
        else:
            return temp

    @staticmethod
    def getRetryTime():
        temp = configPraser.cacheDict.get((configPraser.STR_NETWORK, configPraser.STR_RETRY), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = int(cp.get(configPraser.STR_NETWORK, configPraser.STR_RETRY))
            configPraser.cacheDict[(configPraser.STR_NETWORK, configPraser.STR_RETRY)] = res
            return res
        else:
            return temp

    @staticmethod
    def getOwner():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(configPraser.STR_PROJECT, configPraser.STR_OWNER)

    @staticmethod
    def getRepo():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(configPraser.STR_PROJECT, configPraser.STR_REPO)

    @staticmethod
    def getLimit():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_PROJECT, configPraser.STR_LIMIT))

    @staticmethod
    def getStart():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_PROJECT, configPraser.STR_START))

    @staticmethod
    def getTimeout():
        temp = configPraser.cacheDict.get((configPraser.STR_NETWORK, configPraser.STR_TIMEOUT), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = int(cp.get(configPraser.STR_NETWORK, configPraser.STR_TIMEOUT))
            configPraser.cacheDict[(configPraser.STR_NETWORK, configPraser.STR_TIMEOUT)] = res
            return res
        else:
            return temp

    @staticmethod
    def getSemaphore():
        temp = configPraser.cacheDict.get((configPraser.STR_NETWORK, configPraser.STR_SEMAPHORE), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = int(cp.get(configPraser.STR_NETWORK, configPraser.STR_SEMAPHORE))
            configPraser.cacheDict[(configPraser.STR_NETWORK, configPraser.STR_SEMAPHORE)] = res
            return res
        else:
            return temp

    @staticmethod
    def getDataBase():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(configPraser.STR_DATABASE, configPraser.STR_DATABASE)

    @staticmethod
    def getTopK():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_RECOMMEND, configPraser.STR_TOPK))

    @staticmethod
    def getTestNumber():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_RECOMMEND, configPraser.STR_TEST_NUMBER))

    @staticmethod
    def getReviewerNumber():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_RECOMMEND, configPraser.STR_REVIEWER_NUMBER))

    @staticmethod
    def getFPSRemoveAuthor():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(configPraser.STR_RECOMMEND, configPraser.STR_FPS_REMOVE_AUTHOR) == configPraser.STR_TRUE

    @staticmethod
    def getFPSCtypes():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(configPraser.STR_RECOMMEND, configPraser.STR_FPS_CTYPES) == configPraser.STR_TRUE

    @staticmethod
    def getCommitFetchLoop():
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return int(cp.get(configPraser.STR_PROJECT, configPraser.STR_COMMIT_FETCH_LOOP))

    @staticmethod
    def getApiVersion():
        temp = configPraser.cacheDict.get((configPraser.STR_NETWORK, configPraser.STR_API), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = int(cp.get(configPraser.STR_NETWORK, configPraser.STR_API))
            configPraser.cacheDict[(configPraser.STR_NETWORK, configPraser.STR_API)] = res
            return res
        else:
            return temp

    @staticmethod
    def getIsChangeTriggerByLine():
        temp = configPraser.cacheDict.get((configPraser.STR_RECOMMEND, configPraser.STR_CHANGE_TRIGGER_BY_LINE), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = cp.get(configPraser.STR_RECOMMEND, configPraser.STR_CHANGE_TRIGGER_BY_LINE)
            configPraser.cacheDict[(configPraser.STR_RECOMMEND, configPraser.STR_CHANGE_TRIGGER_BY_LINE)] = res
            return res
        else:
            return temp

    @staticmethod
    def getJVMPath():
        temp = configPraser.cacheDict.get((configPraser.STR_RECOMMEND, configPraser.STR_JVM_PATH), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = cp.get(configPraser.STR_RECOMMEND, configPraser.STR_JVM_PATH)
            configPraser.cacheDict[(configPraser.STR_RECOMMEND, configPraser.STR_JVM_PATH)] = res
            return res
        else:
            return temp

    @staticmethod
    def getStanfordModelPath():
        temp = configPraser.cacheDict.get((configPraser.STR_NLP, configPraser.STR_STANFORD_MODEL_PATH), None)
        if temp is None:
            cp = configparser.ConfigParser()
            cp.read(projectConfig.getConfigPath())
            res = cp.get(configPraser.STR_NLP, configPraser.STR_STANFORD_MODEL_PATH)
            configPraser.cacheDict[(configPraser.STR_NLP, configPraser.STR_STANFORD_MODEL_PATH)] = res
            return res
        else:
            return temp

    #封装获取configParser方法
    @staticmethod
    def get(keyPre='', key=''):
        cp = configparser.ConfigParser()
        cp.read(projectConfig.getConfigPath())
        return cp.get(keyPre, key)

    @staticmethod
    def getMongoDBHost():
        return configPraser.get(configPraser.STR_MONGODB, configPraser.STR_HOST)

    @staticmethod
    def getMongoDBPort():
        return configPraser.get(configPraser.STR_MONGODB, configPraser.STR_PORT)

    @staticmethod
    def getMongoDBDatabaseName():
        return configPraser.get(configPraser.STR_MONGODB, configPraser.STR_DB_NAME)


    @staticmethod
    def getTimeRangeTuple() -> ():
        date = (int(configPraser.get(configPraser.STR_INDEX, configPraser.STR_START_YEAR)),
                int(configPraser.get(configPraser.STR_INDEX, configPraser.STR_START_MONTH)),
                int(configPraser.get(configPraser.STR_INDEX, configPraser.STR_END_YEAR)),
                int(configPraser.get(configPraser.STR_INDEX, configPraser.STR_END_MONTH))
                )
        return date

    @staticmethod
    def getUpdateTime():
        return configPraser.get(configPraser.STR_INDEX, configPraser.STR_UPDATE_TIME)

if __name__ == '__main__':
    print(configPraser.getPrivateToken())

