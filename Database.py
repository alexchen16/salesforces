__author__ = 'chenlei'

import MySQLdb


class Database:

    host = 'localhost'
    user = 'root'
    password = ''
    db = 'salesforce'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()
        print 'Connect mysql server successfully'

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except TypeError as e:
            print(e)
            self.connection.rollback()

    def insert_many(self, query):
        try:
            print 'query',query
            self.cursor.executemany(query)

            self.connection.commit()
        except TypeError as e:
            print(e)
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


