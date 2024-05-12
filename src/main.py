import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSet Factory", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":factory: DataSet Factory", anchor=False)

topCol1, topCol2 = st.columns([0.75,0.25])
bottomCol1, bottomCol2, bottomCol3 = st.columns([0.3,0.4,0.3])

def uploadJsonFile():
    with bottomCol2:
        uploadedFile = st.file_uploader("Load a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in json / jsonl format",)
        if st.button(":outbox_tray: Load dataset"):
            if uploadedFile is not None:
                Mainwindow(uploadedFile)
            else:
                st.toast(":warning: You must choose a file to upload !")

def Mainwindow(uploadedFile):
    with topCol1:
        st.header(":pushpin: " + uploadedFile.name)
        df = pd.read_json(uploadedFile) # some JSON needs the args lines=True and some not, depends on the JSON file format
        st.dataframe(df, use_container_width=True, height=495)
    with topCol2:
        st.header(":clipboard: DataSet Informations")
        with st.container(border=True):
            st.write("Rows: ", df.shape[0])
            st.write("Columns: ", df.shape[1])
            st.write("Columns Names: ", df.columns.tolist())
            st.write("Columns Unique Values: ", df.nunique())

uploadJsonFile()