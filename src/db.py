import streamlit as st
import pandas as pd
import numpy as np
import sqlite3


con = sqlite3.connect("dataset.db", check_same_thread=False, timeout=10000)
cursor = con.cursor()
lastSqlQuery =""
allCols = []

# returns a df from a sql query
def GetDfFromDb(name, sql):
    global lastSqlQuery
    global allCols
    if sql == "":
        sqlcol = " "
        for col in allCols:
            sqlcol += col
            if col != allCols[-1]:
                sqlcol+= ", "
        sql = '''SELECT''' + sqlcol + " FROM "+ name
        lastSqlQuery = sql
    
    elif sql == "last" :
        sql = lastSqlQuery
    
    else : 
        lastSqlQuery = sql
    
    df = pd.read_sql_query(sql, con)
    if 'isValidate' in df.columns:
        df["isValidate"] = df["isValidate"].replace([1], True)
        df["isValidate"] = df["isValidate"].replace([0], False)
    return df

# normalise database
def Normalize(name, df):
    cursor.execute("DELETE FROM "+name+" WHERE id = id")
    
    for row in range(len(df)):
        sqlinsert = '''INSERT INTO '''+name+" VALUES "
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
def CreateTable(name, df):
    formated_name = name.replace("-", "_") # sqlite doesnt support '-' in table name
    global allCols
    col = len(df.columns)
    
    sqlcreate = '''CREATE TABLE '''+formated_name+" ( id INTEGER PRIMARY KEY AUTOINCREMENT"
    allCols.clear()
    for col in df.columns:
        allCols.append(col)
        sqlcreate += ", " + col + " VARCHAR(500)" 
    sqlcreate+=", isValidate BOOLEAN ) "
    allCols.append("isValidate")

    cursor.execute('''DROP Table IF EXISTS '''+formated_name)
    cursor.execute(sqlcreate)

    for row in range(len(df)):
        sqlinsert = '''INSERT INTO '''+formated_name+" VALUES "
        sqlinsert += ('(%a, "')%row
        for col in range(len(df.columns)):
            sqlinsert += (df.iloc[row,col]).replace('"', '""')
            if col != len(df.columns)-1:
                sqlinsert += '", "'
        sqlinsert += '", FALSE)'
        cursor.execute(sqlinsert)

    return GetDfFromDb(formated_name,"")

# filtrates the database
# searching : liste d'expression / colu : liste de colonnes (name of columns)
# returns a df with wanted values
def SearchInDB(name, searching, colu):
    if not colu or len(colu) == 0:
        return GetDfFromDb(name,"")
    if not searching or len(searching) == 0:
        searching[0]=""
    sqlcol = " "
    for col in colu:
        sqlcol += col
        if col != colu[-1]:
            sqlcol+= ", "

    sql = '''SELECT''' + sqlcol + " FROM "+name
    
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

    return GetDfFromDb(name,sql)

# set a row as verified 
# row(int), throwback(bool) (get the updated dataframe if True)
# returns df if throwback = True
def Validate(name, row, throwBack = False):
    con.execute("SELECT isValidate FROM "+name+" WHERE id = " + str(row))
    result = cursor.fetchall()
    if result == True:
        sql = '''UPDATE '''+name+" SET isValidate = FALSE WHERE id = " + str(row)
    sql = '''UPDATE '''+name+" SET isValidate = TRUE WHERE id = " + str(row)
    result = con.execute(sql)
    con.commit()

    if throwBack :
        return GetDfFromDb(name, "last")


# update a row
# row (int), col (string/int), value (string/int), throwBack(True to get the updated df)
# returns updated df if throwback = True
def UpdateRow(name, row, col, value, throwBack = False):
    global allCols
    refInt = 2
    value = value.replace('"', '""')
    if type(col) == type(refInt):
        sql = '''UPDATE '''+name+" SET "+allCols[col]+' = "'+value+'" WHERE id = '+str(row)
    else : 
        sql = '''UPDATE '''+name+" SET "+col+' = "'+value+'" WHERE id = '+str(row)
    cursor.execute(sql)
    con.commit()

    if throwBack:
        return GetDfFromDb(name,"last")

# delete a row
# row (int), throwBack(bool) (returns a df if True)
# returns the updated df if throwBack = True
def DeleteRow(name, row, throwBack):
    global lastSqlQuery
    sql='''DELETE FROM '''+name+" WHERE id = "+str(row)
    cursor.execute(sql)
    last = lastSqlQuery
    Normalize(GetDfFromDb(name,""))
    lastSqlQuery = last
    con.commit()

    if throwBack:
        return GetDfFromDb(name,"last")

# add a row (with a defined id)
# listValues (list of values (string) in columns that are not id and isValidate), valid (bool)( is Validate), id(int)(column where to set the value)
def AddRowWithId(name, listValues, id, valid):        
    sqlInfo = ""+str(id)
    for ex in listValues:
        sqlInfo+=", \""+ex.replace('"', '""').replace("'","''")+"\" "
    if valid:
        sqlInfo+=", TRUE"
    else :
        sqlInfo+=", FALSE"
    sql = '''INSERT INTO '''+name+" VALUES( "+sqlInfo+" )"
    cursor.execute(sql)

# add a row
# listValues (strings), valid (bool)(isValidate),row (int), force (bool) (force row position, move all other data after to free the row), replace (bool)(replace values at row row)
#resturns the updated database
def AddRow(name, listValues, valid = False, row = None, force = False, replace = False):
    global lastSqlQuery
    last = lastSqlQuery
    df = GetDfFromDb(name, "")
    lastSqlQuery = last
    
    if row == None :
        row = len(df)
    else :
        cursor.execute('''SELECT * FROM '''+name+" WHERE id ="+str(row))
        result = cursor.fetchall()
        st.write(result)
        if result :
            if force :
                cursor.execute("UPDATE "+name+" SET id = id+"+str(len(df)+1)+" WHERE id BETWEEN "+str(row) +" AND " +str(len(df)))
                cursor.execute("UPDATE "+name+" SET id = id-"+str(len(df)-1)+" WHERE id BETWEEN "+str(len(df)) +" AND " +str(len(df)*2+2))
            elif replace :
                for i in range(len(listValues)):
                    UpdateRow(name,row, i, listValues[i])
                GetDfFromDb(name,"last")
                return
            else :
                GetDfFromDb(name,"last")
                return
        elif row > len(df) :
            row = len(df)

    AddRowWithId(name,listValues, row, valid)
    con.commit()
    
    return GetDfFromDb(name,"last")

# add a column
# Colname (string), value (string)
# returns the updated df
def AddColumn(name, Colname, value):
    global allCols
    global lastSqlQuery
    allCols.append(name)
    cursor.execute("ALTER TABLE "+name+" ADD "+Colname+" VARCHAR(500)")
    cursor.execute("UPDATE "+name+" SET "+Colname+" = \""+value+"\" WHERE id = id")
    con.commit()

    return GetDfFromDb(name, "")
