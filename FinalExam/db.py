import mysql
import mysql.connector
from mysql.connector import MySQLConnection

user_mysql = 'root'
password_mysql = '111'

class DB(object):
    def __init__(self, host='127.0.0.1', login = user_mysql, password=password_mysql, db='mysql'):
        self.host = host
        self.login = login
        self.password = password
        self.db = db
        self.port = 3306
        self.connector = self.get_connect()
        self.working_db = ''

    def get_connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(host=self.host, db=self.db, user=self.login, password=self.password)
        except:
            print('Connection err')
        return connection

    def get_cursor(self, conn):
        cursor = None
        try:
            cursor = conn.cursor()
        except:
            print('Cursor error')
        return cursor

db = DB()








