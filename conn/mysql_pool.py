from .pymysqlpool import ConnectionPool
class MysqlPool:

    Config = {
        "A210": {
            "pool_name":"a210",
            "host": "123.56.7.210",
            "user": "analysis",
            "password": "j2Gx4amZEQ2o",
            "database": "analysis",
            "port": 33071,

        },
        "Post": {
            "pool_name":"post",
            "host": "219.239.89.88",
            "user": "120ask_read",
            "password": "FnSKcZfi6Wnj18jRBf",
            "database": "post",
            "port": 11113,

        },
        "Local": {
            "pool_name":"local",
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "tag",
            "port": 3306,

        },
        "Ad":{
            "pool_name":"ad",
            "host": "47.93.33.215",
            "user": "ad_user",
            "password": "gjasu$%ada",
            "database": "ad",
            "port": 3306,
        }
    }

    def __init__(self,configFlag='Local'):
        self.configFlag = configFlag

    def connection_pool(self,configFlag='Local'):
        pool = ConnectionPool(**self.Config[self.configFlag])
        return pool

    def fetchone(self,sql,params):
        with self.connection_pool().cursor() as cursor:
            cursor.execute(sql,params)
            return cursor.fetchone()

    def fetchall(self,sql,params):
        with self.connection_pool().cursor() as cursor:
            cursor.execute(sql,params)
            return cursor.fetchall()

    def insert(self,sql,params):
        with self.connection_pool().cursor() as cursor:
            return cursor.execute(sql,params)


    def update(self,sql,params):
        with self.connection_pool().cursor() as cursor:
            return cursor.execute(sql,params)

    def delete(self,sql,params):
        with self.connection_pool().cursor() as cursor:
            return cursor.execute(sql,params)
