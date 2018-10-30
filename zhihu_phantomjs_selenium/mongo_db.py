#mongo
import pymongo
import setting

class MongoOrm(object):
    def __init__(self):
        self.database = pymongo.MongoClient(setting.Mongo['host'])
        self.db = self.database[setting.Mongo['db']][setting.Mongo['table']]
    def insert_into_db(self,con):
        self.db.insert_one(con)