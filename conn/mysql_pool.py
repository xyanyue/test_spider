from .pymysqlpool import ConnectionPool
class MysqlPool:

    Config = {
        "Local": {
            "pool_name":"local",
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "tag",
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
