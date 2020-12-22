import pymongo

from pymongo import MongoClient

from source.config.configPraser import configPraser


class MongoDBHelper:

    def __init__(self):
        self.initConnect()
        self.client = self.initConnect()
        self.db = self.client[configPraser.getMongoDBDatabaseName()]

    def initConnect(self) -> MongoClient:
        client = pymongo.MongoClient(host=configPraser.getMongoDBHost(), port=int(configPraser.getMongoDBPort()))
        return client

    def writeIntoDatabase(self, collectionName='', data={}):
        collection = self.getCollection(collectionName)
        collection.insert_one(data)

    def createCollection(self, collectionName=''):
        self.db.create_collection(collectionName)

    def listCollectionNames(self):
        return self.db.list_collection_names()

    def getCollection(self, collectionName=''):
        return self.db[collectionName]

#使用单例模式，减少对数据库的连接
singleton = MongoDBHelper()




