import mysql
import mysql.connector
from mysql.connector import MySQLConnection
import os

user_mysql = 'root'
password_mysql = '111'
name_db = 'Final_Test'
# name_db = 'mysql'

#
# con = mysql.connector.connect(user=user_mysql, password=password_mysql)
# cur = con.cursor()
# s= 'select'
# cur.execute(s)
# cur.fetchall
def read_file_by_line(file_name):
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line

class DB(object):
    def __init__(self, host='127.0.0.1', login = user_mysql, password=password_mysql, db=name_db):
        self.host = host
        self.login = login
        self.password = password
        self.db = db
        self.port = 3306
        self.connector = self.get_connect()
        print(self.connector)
        self.cur = self.get_cursor(self.connector)
        self.working_db = ''

    def get_connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(host=self.host, db='', user=self.login, password=self.password)
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

    def is_db_exists(self):
        try:
            query = 'SHOW databases;'
            cur = self.cur
            cur.execute(query)
            # data = cur.fetchall()
            # print(data, self.db)
            for _ in cur.fetchall():
                if _[0] == self.db:
                    return True
            return False
        except:
            print('err')

    def create_db(self):
        try:
            cur = self.cur
            if not self.is_db_exists():
                # cur=self.cur
                query = 'CREATE database {};'.format(self.db)
                cur.execute(query)
            query = 'USE {}'.format(self.db)
            cur.execute(query)
            print(cur, self.cur)
            #self.cur = cur
        except:
            print('Error: create db')

    def create_table(self):
        cur = self.cur
        try:
            query = 'DROP TABLE alesya;'
            cur.execute(query)
            query = 'CREATE TABLE alesya(file_name VARCHAR(60) UNIQUE NOT NULL PRIMARY KEY, hash_sum VARCHAR(64) NOT NULL);'
            cur.execute(query)
        except:
            print('Error: create table')

    def fill_table(self):
        cur_parth = os.getcwd()  # directory with project
        command = 'cd /home/{}; md5sum * >{}/list.txt'.format('pyautomation', cur_parth)
        os.system(command)
        file_gen = read_file_by_line('list.txt')
        i=0
        cur = self.cur
        for line in file_gen:
            i+=1
            if i <3:
                continue
            data = line.split()
            print(data[0], data[1])
            query = 'INSERT INTO alesya(file_name, hash_sum) VALUES(\'{}\', \'{}\');'.format(data[1], data[0])
            print(query)
            cur.execute(query)
            try:
                pass
                # query = 'INSERT INTO alesya(file_name, hash_sum) VALUES(\'{}\', \'{}\');'.format(data[1], data[0])
                # print(query)
                # cur.execute(query)
            except:
                print('Error: insert into table')


    def close(self):
        self.connector.close()





db = DB()
db.is_db_exists()
db.create_db()
db.create_table()
db.fill_table()
db.close()








