import streamlit as st
import os
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSet Factory - Upload a file", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":outbox_tray: Import a file", anchor=False)

topCol0, topCol1 = st.columns([0.75,0.25])
bottomCol0, bottomCol1, bottomCol2 = st.columns([0.3,0.4,0.3])

# https://blog.streamlit.io/editable-dataframes-are-here/

def Mainwindow(uploadedFile): #load the uploaded in file into the dataset
    with topCol0:
        st.header(":pushpin: " + uploadedFile.name)
        match os.path.splitext(os.path.basename(uploadedFile.name))[1]:
            case ".json":
                df = pd.read_json(uploadedFile) 
            case ".jsonl":
                df = pd.read_json(uploadedFile, lines=True)
            #no default needed st.file_uploader ensure that it is the correct file extension

        st.dataframe(df, use_container_width=True, height=495)
        CreateDB(df)
    with topCol1:
        st.header(":clipboard:  Informations")
        with st.container(border=True):
            st.write("Rows: ", df.shape[0])
            st.write("Columns: ", df.shape[1])
            st.write("Columns Names: ", df.columns.tolist())
            st.write("Columns Unique Values: ", df.nunique())

def uploadJsonFile(): #upload a file to display it in a datatset
    with bottomCol1:
        uploadedFile = st.file_uploader("Load a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in json / jsonl format",)
        if st.button(":outbox_tray: Load dataset"):
            if uploadedFile is not None:
                Mainwindow(uploadedFile)
            else:
                st.toast(":warning: You must choose a file to upload !")

uploadJsonFile()
