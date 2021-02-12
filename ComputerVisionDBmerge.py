import sqlite3

class DB_merge():
    def __init__(self, dname):
        self.db=dname
        self.outputs = []

    def db_output(self, tableName):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        outPut_table = '''SELECT * FROM {}'''.format(tableName)
        c.execute(outPut_table)
        self.outputs.append(c.fetchall())
        c.close()
        conn.close()

    def db_tableList(self, exceptName):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        list_table = '''SELECT name FROM sqlite_master WHERE TYPE="table"'''
        c.execute(list_table)
        tableList = c.fetchall()
        c.close()
        conn.close()

        return [v[0] for v in tableList if v[0] != exceptName and '_TMP' not in v[0]]

    def db_allValues(self, tableNames, keyName):
        tableNames = [v for v in tableNames if v != 'all_' + keyName]
        tableNames = [v for v in tableNames if '_TMP' not in v]

        conn=sqlite3.connect(self.db)
        c = conn.cursor()

        article = []
        for tbN in tableNames:
            outPut_table = '''SELECT {} FROM {}'''.format(keyName, tbN)

            c.execute(outPut_table)
            _tmp = c.fetchall()

            for t in _tmp:
                article.append(t[0])

        create_table = '''CREATE TABLE IF NOT EXISTS all_{0} ({0}, PRIMARY KEY({0}))'''.format(keyName)
        c.execute(create_table)
        sql = 'insert or ignore into all_{0} ({0}) values (?)'.format(keyName)
        for a in article:
            c.execute(sql, (a,))
        conn.commit()
        c.close()
        conn.close()

    def db_allValues_table_Query(self, tableNames, keyName):
        select_tables = ''
        for tbN in tableNames[1:]:
            select_tables += 'UNION SELECT ' + keyName + ' FROM ' + tbN + ' '

        outPut_table = 'SELECT {} FROM {} {}'.format(keyName, tableNames[0], select_tables)
        return outPut_table

    def db_concat(self, mainTableName, tableNames, keyName):
        conn=sqlite3.connect(self.db)
        c = conn.cursor()
        
        c.execute('''DROP TABLE IF EXISTS _TMP0''')
        c.execute('''DROP TABLE IF EXISTS _TMP1''')
        c.execute('''DROP TABLE IF EXISTS _TMP2''')

        #create_table = '''CREATE TABLE IF NOT EXISTS _TMP1 AS SELECT * FROM {}'''.format(mainTableName)
        column_names = ''
        for tb in tableNames:
            column_names += tb + ', '
        column_names = column_names[:-2]
        create_table = '''CREATE TABLE IF NOT EXISTS _TMP1 (p_name, {})'''.format(column_names)
        c.execute(create_table)
        c.execute('''insert into _TMP1 (p_name) SELECT p_name from {}'''.format(mainTableName))

        for index, tbN in enumerate(tableNames):
            print(tbN)
            _original_tbN = tbN

            table_check = '''SELECT * FROM {}'''.format(tbN)
            c.execute(table_check)
            _tmpRes = c.fetchall()
            #print(_tmpRes[0])
            if len(_tmpRes[0]) > 2:
                tbN = '_TMP2'
                create_Ttable = '''CREATE TABLE IF NOT EXISTS _TMP2 (p_name, {})'''.format(_tmpRes[0][1])
                c.execute(create_Ttable)
                conn.commit()
                for _tR in _tmpRes:
                    _toScored = _tR[2]
                    if _tR[2] == 'True':
                        _toScored = 1
                    elif _tR[2] == 'False':
                        _toScored = 0
                    c.execute('''insert into _TMP2 (p_name, {}) values (?,?)'''.format(_tR[1]), (_tR[0], _toScored))
                conn.commit()
            

            #select_tables = 'LEFT OUTER JOIN ' + tbN + ' ON _TMP' + str((index+1)%2) + '.' + keyName + '=' + tbN + '.' + keyName + ' '
            #create_table = '''CREATE TABLE IF NOT EXISTS _TMP{} AS SELECT * FROM {} {}'''.format(index%2,'_TMP{}'.format(str((index+1)%2)),select_tables)
            c.execute('''SELECT * FROM {}'''.format(tbN))
            resValues = c.fetchall()
            for rv in resValues:
                _key, _value = rv[0], rv[1]
                create_table = '''UPDATE _TMP1 SET {} = '{}' WHERE {} = '{}' '''.format(_original_tbN,_value,keyName, _key)
                c.execute(create_table)
                conn.commit()
            #c.execute('''DROP TABLE _TMP{}'''.format((index+1)%2))
            c.execute('''DROP TABLE IF EXISTS _TMP2''')
            #conn.commit()


        #outPut_table = '''SELECT * FROM ({}) {})'''.format(mainTableName, select_tables)
        #print(outPut_table)
        #c.execute('''SELECT * FROM _TMP{}'''.format(index%2))
        c.execute('''SELECT * FROM _TMP1''')
        results = c.fetchall()
#        for _d in c.description[::2]:
#            print(_d[0])
        c.close()
        conn.close()
        for rs in results:
            print(rs)

