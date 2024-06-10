import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


con = sqlite3.connect("dataset.db", check_same_thread=False)
cursor = con.cursor()
lastSqlQuery =""
allCols = []

# returns a df from a sql query
def GetDfFromDb(sql):
    global lastSqlQuery
    global allCols
    if sql == "":
        sqlcol = " "
        for col in allCols:
            sqlcol += col
            if col != allCols[-1]:
                sqlcol+= ", "
        sql = '''SELECT''' + sqlcol + " FROM dataset"
        lastSqlQuery = sql
    
    elif sql == "last" :
        sql = lastSqlQuery
    
    else : 
        lastSqlQuery = sql
    
    df = pd.read_sql_query(sql, con)
    return df

# normalise database
def Normalize(df):
    cursor.execute("DELETE FROM dataset WHERE id = id")
    
    for row in range(len(df)):
        sqlinsert = '''INSERT INTO dataset VALUES '''
        sqlinsert += ('(%a, ')%row
        for col in range(len(df.columns)):
            if df.iloc[row,col] == 0:
                sqlinsert += "FALSE"
            elif df.iloc[row,col] == 1:
                sqlinsert +="TRUE"
            else:
                sqlinsert += '"'+(df.iloc[row,col]).replace('"', '""')+'"'
            if col != len(df.columns)-1:
                sqlinsert += ', '
        sqlinsert += ')'
        cursor.execute(sqlinsert)

# creates a sql database from df
def CreateTable(df):
    global allCols
    col = len(df.columns)
    
    sqlcreate = '''CREATE TABLE dataset ( id INTEGER PRIMARY KEY AUTOINCREMENT'''
    allCols.clear()
    for col in df.columns:
        allCols.append(col)
        sqlcreate += ", " + col + " VARCHAR(500)" 
    sqlcreate+=", isValidate BOOLEAN ) "
    allCols.append("isValidate")

    cursor.execute('''DROP Table IF EXISTS dataset''')
    cursor.execute(sqlcreate)

    for row in range(len(df)):
        sqlinsert = '''INSERT INTO dataset VALUES '''
        sqlinsert += ('(%a, "')%row
        for col in range(len(df.columns)):
            sqlinsert += (df.iloc[row,col]).replace('"', '""')
            if col != len(df.columns)-1:
                sqlinsert += '", "'
        sqlinsert += '", FALSE)'
        cursor.execute(sqlinsert)

    return GetDfFromDb("")

def CreateDB(df): #doesn't exists anymore
    return CreateTable(df)

# filtrates the database
# searching : liste d'expression / colu : liste de colonnes (name of columns)
# returns a df with wanted values
def SearchInDB(searching, colu):
    if not colu or len(colu) == 0:
        return GetDfFromDb("")
    if not searching or len(searching) == 0:
        searching[0]=""
    sqlcol = " "
    for col in colu:
        sqlcol += col
        if col != colu[-1]:
            sqlcol+= ", "

    sql = '''SELECT''' + sqlcol + " FROM dataset"
    
    sql+= " WHERE "

    for col in colu:
        sql += '('
        for ex in searching:
            sql += col + ' LIKE "'
            sql += "%"+ex.replace('"', '""')+"%"
            if ex != searching[-1]:
                sql += '" OR "'
        sql += '"'

        if (col != colu[-1]):
            sql+=') OR ('
    sql+=')'

    return GetDfFromDb(sql)

# set a row as verified 
# row(int), throwback(bool) (get the updated dataframe if True)
# returns df if throwback = True
def Validate(row, throwBack = False):
    con.execute("SELECT isValidate FROM dataset WHERE id = " + str(row))
    result = cursor.fetchall()
    if result == True:
        sql = '''UPDATE dataset SET isValidate = FALSE WHERE id = ''' + str(row)
    sql = '''UPDATE dataset SET isValidate = TRUE WHERE id = ''' + str(row)
    result = con.execute(sql)
    con.commit()

    if throwBack :
        return GetDfFromDb("last")


# update a row
# row (int), col (string/int), value (string/int), throwBack(True to get the updated df)
# returns updated df if throwback = True
def UpdateRow(row, col, value, throwBack = False):
    global allCols
    refInt = 2
    value = value.replace('"', '""')
    if type(col) == type(refInt):
        sql = '''UPDATE dataset SET '''+allCols[col]+' = "'+value+'" WHERE id = '+str(row)
    else : 
        sql = '''UPDATE dataset SET '''+col+' = "'+value+'" WHERE id = '+str(row)
    cursor.execute(sql)
    con.commit()

    if throwBack:
        return GetDfFromDb("last")

# delete a row
# row (int), throwBack(bool) (returns a df if True)
# returns the updated df if throwBack = True
def DeleteRow(row, throwBack):
    global lastSqlQuery
    sql='''DELETE FROM dataset WHERE id = '''+str(row)
    cursor.execute(sql)
    last = lastSqlQuery
    Normalize(GetDfFromDb(""))
    lastSqlQuery = last
    con.commit()

    if throwBack:
        return GetDfFromDb("last")

# add a row (with a defined id)
# listValues (list of values (string) in columns that are not id and isValidate), valid (bool)( is Validate), id(int)(column where to set the value)
def AddRowWithId(listValues, id, valid):        
    sqlInfo = ""+str(id)
    for ex in listValues:
        sqlInfo+=", \""+ex.replace('"', '""').replace("'","''")+"\" "
    if valid:
        sqlInfo+=", TRUE"
    else :
        sqlInfo+=", FALSE"
    sql = '''INSERT INTO dataset VALUES( '''+sqlInfo+" )"
    cursor.execute(sql)

# add a row
# listValues (strings), valid (bool)(isValidate),row (int), force (bool) (force row position, move all other data after to free the row), replace (bool)(replace values at row row)
#resturns the updated database
def AddRow(listValues, valid = False, row = None, force = False, replace = False):
    global lastSqlQuery
    last = lastSqlQuery
    df = GetDfFromDb("")
    lastSqlQuery = last
    
    if row == None :
        row = len(df)
    else :
        cursor.execute('''SELECT * FROM dataset WHERE id ='''+str(row))
        result = cursor.fetchall()
        st.write(result)
        if result :
            if force :
                cursor.execute("UPDATE dataset SET id = id+"+str(len(df)+1)+" WHERE id BETWEEN "+str(row) +" AND " +str(len(df)))
                cursor.execute("UPDATE dataset SET id = id-"+str(len(df)-1)+" WHERE id BETWEEN "+str(len(df)) +" AND " +str(len(df)*2+2))
            elif replace :
                for i in range(len(listValues)):
                    UpdateRow(row, i, listValues[i])
                GetDfFromDb("last")
                return
            else :
                GetDfFromDb("last")
                return
        elif row > len(df) :
            row = len(df)

    AddRowWithId(listValues, row, valid)
    con.commit()
    
    return GetDfFromDb("last")

# add a column
# name (string), value (string)
# returns the updated df
def AddColumn(name, value):
    global allCols
    global lastSqlQuery
    allCols.append(name)
    cursor.execute("ALTER TABLE dataset ADD "+name+" VARCHAR(500)")
    cursor.execute("UPDATE dataset SET "+name+" = \""+value+"\" WHERE id = id")
    con.commit()

    return GetDfFromDb("")
