import streamlit as st
import os
import pandas as pd
import numpy as np
import db

st.set_page_config(page_title="DataSet Factory - Edit a DataSet", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":pencil: Edit a DataSet", anchor=False)

# Load the temporary file path from session state
uploadedFile = st.session_state.get('uploadedFile', None)
df = st.session_state.get('dataframe', None)

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

            dfUpdate = db.GetDfFromDb(tableName,"")

            dataset_col, info_col = st.columns([3, 1])
            
            with dataset_col:
                st.header(f":pushpin: {fileName} Dataset")
                st.dataframe(dfUpdate, use_container_width=True, height=500)
                
            with info_col:
                st.header(":clipboard: Informations")
                st.write("Rows: ", df.shape[0])
                st.write("Columns: ", df.shape[1])
                st.write("Columns Names: ", df.columns.tolist())
                st.write("Columns Unique Values: ", df.nunique())

            Col0, Col1, Col2 = st.columns([0.35, 0.35, 0.3])
            
            with Col0:
                row_number = st.number_input("Row To Modify / Add", min_value=0, max_value=df.shape[0]-1, step=1)
                if st.button(":heavy_plus_sign: Add a row"):
                    tableRow = [""] * df.shape[1]
                    dfUpdate = db.AddRow(tableName,tableRow,False,row_number,True)
                    st.experimental_rerun()
                if st.button(":heavy_multiplication_x: Delete selected Row", help="Delete the row specified above"):
                    dfUpdate = db.DeleteRow(tableName, row_number, True)
                    st.experimental_rerun()
                if st.button(":heavy_check_mark: Validate selected Row", help="Validate the row specified above"):
                    dfUpdate = db.Validate(tableName, row_number, True)
                    st.experimental_rerun()
                if st.button(":heavy_multiplication_x: Unvalidate Row"):
                    dfUpdate = db.Unvalidate(tableName, row_number, True)
                    st.experimental_rerun()
                if st.button(":heavy_check_mark: Validate all Row", help="Validate all Row"):
                    for x in range(df.shape[0]):
                        db.Validate(tableName, x)
                    dfUpdate = db.GetDfFromDb(tableName, "")
                    st.experimental_rerun()
                
            with Col1:
                col = st.selectbox("Columns where you want to Replace", options=df.columns.values)
                valueToChange = st.text_input("The new value to replace in the dataset", value="")
                if st.button(":heavy_check_mark: Change Value", help="Change the value"):
                    dfUpdate = db.UpdateRow(tableName, row_number, col, valueToChange)
                    st.experimental_rerun()

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


