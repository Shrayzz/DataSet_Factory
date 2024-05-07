import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSet Factory", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":factory: DataSet Factory")

col1, col2 = st.columns(2)

def uploadJsonFile():
    with st.container(border=True):
        uploadedFile = st.file_uploader("Upload a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in json / jsonl format",)
    if st.button("Submit"):
        if uploadedFile is not None:
            Mainwindow(uploadedFile)
        else:
            st.toast(":warning: Please upload a file")

def Mainwindow(uploadedFile):
    with col1:
        st.header(uploadedFile.name)
        df = pd.read_json(uploadedFile, lines=True)
        st.dataframe(df, use_container_width=True)
    with col2:
        st.header("Actions")

    


    # with st.container(border=True):
    #     st.header(uploadedFile.name)
    #     df = pd.read_json(uploadedFile, lines=True)
    #     st.dataframe(df, use_container_width=True)

uploadJsonFile()