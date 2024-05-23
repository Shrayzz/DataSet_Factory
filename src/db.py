import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

con = sqlite3.connect("dataset.db", check_same_thread=False)

def GetDfFromDb(sql, df):
    if sql == "":
        sqlcol = " "
        for col in df.columns:
            sqlcol += col
            if col != df.columns[-1]:
                sqlcol+= ", "

        sql = '''SELECT''' + sqlcol + " FROM dataset"
    con.commit()
    df = pd.read_sql_query(sql, con)
    return df

def CreateDB(df):

    col = len(df.columns)
    
    sqlcreate = '''CREATE TABLE dataset ( id INTEGER PRIMARY KEY AUTOINCREMENT'''

    for col in df.columns:
        sqlcreate += ", " + col + " VARCHAR(500)" 
    sqlcreate+=", isValidate BOOLEAN ) "

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
        sqlinsert += '", FALSE)'
        cursor.execute(sqlinsert)

    
    sqlcol = " "
    for col in df.columns:
        sqlcol += col
        if col != df.columns[-1]:
            sqlcol+= ", "

    sql = '''SELECT''' + sqlcol + ", isValidate FROM dataset"
    return GetDfFromDb(sql, df)

# searching : liste d'expression / colu : liste de colonnes
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

    sql = '''SELECT''' + sqlcol + " FROM dataset"
    
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
    return GetDfFromDb(sql, df)

def Validate(row):
    cursor = con.cursor()
    con.execute("SELECT isValidate FROM dataset WHERE id = " + str(row))
    result = cursor.fetchall()
    
    st.write("SELECT isValidate FROM dataset WHERE id = " + str(row))
    st.write(result)
    if result == True:
        sql = '''UPDATE dataset SET isValidate = FALSE WHERE id = ''' + str(row)
    sql = '''UPDATE dataset SET isValidate = TRUE WHERE id = ''' + str(row)
    result = con.execute(sql)
    con.commit()

