import mysql
import mysql.connector
import os
import sys

def read_file_by_line(file_name):
    with open(file_name, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line

class DB(object):
    def __init__(self, host, login, password, db):
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
            connection = mysql.connector.connect(host=self.host, db='', user=self.login, password = self.password)
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
            for _ in cur.fetchall():
                if _[0] == self.db:
                    return True
            return False
        except:
            print('Error: Show databases')

    def create_db(self):
        try:
            cur = self.cur
            if not self.is_db_exists():
                query = 'CREATE database {};'.format(self.db)
                cur.execute(query)
            query = 'USE {}'.format(self.db)
            cur.execute(query)
            return True
        except:
            print('Error: create db')
            return False

    def create_table(self):
        cur = self.cur
        try:
            try:
                query = 'DROP TABLE alesya;'
                cur.execute(query)
            except:
                print('Warning: drop table')
            query = 'CREATE TABLE alesya(file_name VARCHAR(60) UNIQUE NOT NULL PRIMARY KEY, hash_sum VARCHAR(64) NOT NULL);'
            cur.execute(query)
            return True
        except:
            print('Error: create table')
            return False

    def fill_table(self):
        cur_parth = os.getcwd()
        command = 'cd /home/{}; md5sum * >{}/list.txt'.format('pythonista', cur_parth)
        os.system(command)
        file_gen = read_file_by_line('list.txt')
        cur = self.cur
        for line in file_gen:
            data = line.split()
            print(data[0], data[1])
            try:
                query = 'INSERT INTO alesya(file_name, hash_sum) VALUES(\'{}\', \'{}\');'.format(data[1], data[0])
                cur.execute(query)
                self.connector.commit()
            except:
                print('Error: insert into table')
                self.connector.rollback()

    def close(self):
        self.connector.close()

if __name__ == '__main__':

    name_db = 'Final_Test'

    if not len(sys.argv)==3:
        print('Error: Check params')
    else:
        user_mysql = sys.argv[1]
        password_mysql = sys.argv[2]
        db = DB('127.0.0.1', user_mysql, password_mysql, name_db)
        db.is_db_exists()
        if not db.create_db():
            print('DB did not create')
        else:
            if not db.create_table():
                print('Table did not create')
            else:
                db.fill_table()
                db.close()