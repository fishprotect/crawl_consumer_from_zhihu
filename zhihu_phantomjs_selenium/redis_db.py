#redis数据库的存取
import redis
import setting

class RedisOrm(object):
    def __init__(self):
        self.host = setting.Redis['host']
        self.port=setting.Redis['port']
        self.database=setting.Redis['db']
        self.list_url = setting.Redis['table']
        self.db = redis.Redis(self.host,self.port,self.database)
    def insert_into_db(self,url):
        try:
            self.db.lrem(self.list_url,utl,num=0)
        except:
            pass
        self.db.rpush(self.list_url,url)  ##区别rpush(右插，插入到列表的最后)&&lpush(左插，插入到列表的第一位置)
    def select_from_db(self):
        con = self.db.lpop(self.list_url) ##rpop&&lpop
        if con:
            return con.decode('utf-8')
        else:
            return 'None'
