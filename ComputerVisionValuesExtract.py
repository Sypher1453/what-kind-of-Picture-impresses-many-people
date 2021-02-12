import sqlite3
import numpy
import sklearn
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn import neural_network
from sklearn import linear_model
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import r2_score

import glob
import math

class DB_values():
    def __init__(self, dname):
        self.db=dname
        self.valueTags = []
        self.values = None


    def db_extract(self, tableName, keyName):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        
        c.execute('''SELECT * FROM {}'''.format(tableName))
        self.values = c.fetchall()
        c.close()
        conn.close()

        for desc in c.description:
            self.valueTags.append(desc[0])

    def get_values(self):
        return self.values

    def get_tags(self):
        return self.valueTags

def someValueCheck(value, _index):
    if 'gender' in _tags[_index+1]:
        if value == 'Male':
            return 0
        if value == 'Female':
            return 1

    if 'accentColor' in _tags[_index+1]:
        _r = int(value[:2],16)
        _g = int(value[2:4],16)
        _b = int(value[4:],16)
        return [_r, _g, _b, _r*_g, _r*_b, _g*_b, _r*_g*_b]
    return None

