import streamlit as st
import pandas as pd
import numpy as np

st.title(":factory: DataSet Factory")

def uploadJsonFile():
    uploadedFile = st.file_uploader("Upload a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in json / jsonl format")
    if st.button("Submit"):
        if uploadedFile is not None:
            Mainwindow(uploadedFile)
        else:
            st.warning("Please upload a file")


def Mainwindow(uploadedFile):
    with st.container(border=True):
        st.header(uploadedFile.name)
        df = pd.read_json(uploadedFile, lines=True)
        st.dataframe(df, use_container_width=True)


uploadJsonFile()