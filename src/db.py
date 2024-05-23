import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

con = sqlite3.connect("dataset.bd")

def createDB(df):

    col = len(df.columns)
    
    sqlcreate = '''CREATE TABLE dataset ( id INTEGER PRIMARY KEY AUTOINCREMENT'''
    
    print(df.columns)
    for col in df.columns:
        sqlcreate += ", " + col + " VARCHAR(500)" 
    sqlcreate+=" ) "

    cursor = con.cursor()
    
    cursor.execute('''DROP Table IF EXISTS dataset''')
    cursor.execute(sqlcreate)

    for row in range(len(df)):
        sqlinsert = '''INSERT INTO dataset VALUES '''
        sqlinsert += ('(%a, "')%row
        for col in range(len(df.columns)):
            sqlinsert += ((df.iloc[row,col]).replace('"', '""')).replace("'", "''")
            if col != len(df.columns)-1:
                sqlinsert += '", "'
        sqlinsert += '")'
        cursor.execute(sqlinsert)

    con.commit()
    

def SearchInDB(searching, colu, df):
    sqlin = ''' LIKE ("'''
    for ex in searching:
        sqlin += "%"+ex+"%"
        if (ex != searching[-1]):
            sqlin += '", "'
        sqlin+= '")'
    sqlcol = " "
    for col in df.columns:
        sqlcol += col
        if col != df.columns[-1]:
            sqlcol+= ", "

    sql = '''SELECT''' + sqlcol + ", isValidate FROM dataset"
    
    sql+= " WHERE "

    for col in colu:
        #if (len(searching) == 1):
        #    sql += col + ' = "'+ searching[0] +'"'
        #else :
        sql += '('
        for ex in searching:
            sql += col + ' LIKE "'
            sql += "%"+ex+"%"
            if (ex != searching[-1]):
                sql += '" OR "'
        sql += '"'

        if (col != colu[-1]):
            sql+=') OR ('
    sql+=')'
    print(sql)
    df = pd.read_sql_query(sql, con)
    st.write(sql)
    return df
