import urllib.request
import json
import sqlite3
import glob
from PIL import Image
import io
import time

class DB_post():
    def __init__(self, dname):
        self.db=dname

    def add2indexList(self, value):
        print(value)
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        sql = '''INSERT or IGNORE into all_p_name (p_name) VALUES (?)'''
        c.execute(sql,(value,))
        conn.commit()
        c.close()
        conn.close()

    def is_exist(self,value):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        sql = '''SELECT * from all_p_name WHERE p_name = "{}"'''.format(value)
        print(sql)
        c.execute(sql)
        res = c.fetchall()
        c.close()
        conn.close()

        return len(res) > 0

    def db_inputDefault(self, key_name, article):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS {0} (p_name, {0}, value)'''.format('__' + key_name)
        print('ct', create_table)
        c.execute(create_table)
        sql = 'insert into {0} (p_name, {0}, value) values (?,?,?)'.format('__' + key_name)
        print('sql', sql)
        c.execute(sql, article)
        conn.commit()
        c.close()
        conn.close()

        self.add2indexList(article[0])

    def db_input(self, key_name, article):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        create_table = '''CREATE TABLE IF NOT EXISTS {0} (p_name, {0})'''.format('_' + key_name)
        print('ct', create_table)
        c.execute(create_table)
        sql = 'insert into {0} (p_name, {0}) values (?,?)'.format('_' + key_name)
        print('sql', sql)
        c.execute(sql, article)
        conn.commit()
        c.close()
        conn.close()

        self.add2indexList(article[0])

