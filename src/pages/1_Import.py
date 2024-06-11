import db
import streamlit as st
import os
import pandas as pd
import numpy as np
import tempfile

st.set_page_config(page_title="DataSet Factory - Upload a file", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":inbox_tray: Import a file", anchor=False)

topCol0, topCol1 = st.columns([0.75,0.25])

bottomCol0, bottomCol1, bottomCol2 = st.columns([0.3,0.4,0.3])

def uploadJsonFile(): # upload a file to display it in a dataset
    with bottomCol1:
        uploadedFile = st.file_uploader("Load a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in JSON / JSONL format only",)
        if st.button(":inbox_tray: Load a dataset"):
            if uploadedFile is not None:
                
                # Load the data into a DataFrame
                if uploadedFile.name.endswith('.json'):
                    df = pd.read_json(uploadedFile)
                elif uploadedFile.name.endswith('.jsonl'):
                    df = pd.read_json(uploadedFile, lines=True)
                
                # Clean the dataframe to remove any null characters
                df = df.map(lambda x: x.replace('\x00', '') if isinstance(x, str) else x)
                
                # Save the dataframe to the database
                db.CreateTable(uploadedFile.name.replace("-", "_").split('.',1)[0],df)
                
                # Set the DataFrame and uploadedFile in the session state
                st.session_state['uploadedFile'] = uploadedFile
                st.session_state['dataframe'] = df
                
                # Redirect to Edit page
                st.success(":heavy_check_mark: File uploaded successfully, look on Edit tab !")
            else:
                st.warning(":warning: You must choose a file to upload !")

uploadJsonFile()
