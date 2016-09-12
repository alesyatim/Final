import mysql
import mysql.connector
from mysql.connector import MySQLConnection

user_mysql = 'root'
password_mysql = 'exam'

class DB(object):
    def __init__(self, host, user, password, db='mysql'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connector = ''
        self.working_db = ''


    def get_connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(host='localhost', db='mysql', user=user_mysql, password=password_mysql)
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








