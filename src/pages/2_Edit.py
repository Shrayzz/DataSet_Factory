import streamlit as st
import os
import pandas as pd
import numpy as np
import db

st.set_page_config(page_title="DataSet Factory - Edit a DataSet", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":pencil: Edit a DataSet", anchor=False)

topCol0, topCol1 = st.columns([0.75,0.25])

# Load the temporary file path from session state
uploadedFile = st.session_state.get('uploadedFile', None)

def displayDataFrame(uploadedFile, fileName, fileExtension):
    if uploadedFile is not None:
        tableName = uploadedFile.name.replace("-", "_").split('.',1)[0]
        try:
            # Reset file pointer to the beginning
            uploadedFile.seek(0)
            
            if fileExtension == ".json":
                df = pd.read_json(uploadedFile) 
            elif fileExtension == ".jsonl":
                df = pd.read_json(uploadedFile, lines=True)
            else:
                st.error("Unsupported file extension")

            # Clean the dataframe to remove any null characters
            df = df.map(lambda x: x.replace('\x00', '') if isinstance(x, str) else x)
        
            with topCol0:
                st.header(f":pushpin: {fileName} Dataset")
                st.dataframe(db.CreateTable(tableName,df), use_container_width=True, height=495)

            with topCol1:
                st.header(":clipboard: Informations")
                with st.container():
                    st.write("Rows: ", df.shape[0])
                    st.write("Columns: ", df.shape[1])
                    st.write("Columns Names: ", df.columns.tolist())
                    st.write("Columns Unique Values: ", df.nunique())
                    row_number = st.number_input("Row To Modify", min_value=0, max_value=df.shape[0], step=1)
                    if st.button(":heavy_multiplication_x: Delete selected Row", help="Delete the row specified above"):
                        db.DeleteRow(tableName,row_number,throwBack=True)
                    if st.button(":heavy_check_mark: Validate selected Row", help="Validate the row specified above"):
                        db.Validate(tableName,row_number)
                        db.CreateTable(tableName, df) # actualize db 
                    if st.button(":heavy_check_mark: Validate all Row", help="Validate all Row"):
                        db.Validate(tableName,df.shape[0])
                        db.CreateTable(tableName, df) #actualize db
        
        except ValueError as e:
            st.error(f":x: Error reading JSON file: {e}")
            st.error(":x: Ensure the uploaded file is a valid JSON.")
    else:
        st.warning(":warning: No dataset loaded. Please upload a dataset in the Import section.")

if uploadedFile is not None:
    fileName = os.path.splitext(os.path.basename(uploadedFile.name))[0]
    fileExtension = os.path.splitext(os.path.basename(uploadedFile.name))[1]
    displayDataFrame(uploadedFile, fileName, fileExtension)
else:
    st.warning(":warning: No dataset loaded. Please upload a dataset in the Import section.")
