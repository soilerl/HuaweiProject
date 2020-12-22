import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
print(client.list_database_names())