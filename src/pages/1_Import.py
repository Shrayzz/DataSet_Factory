import db
import streamlit as st
import os
import pandas as pd
import numpy as np
import tempfile

st.set_page_config(page_title="DataSet Factory - Upload a file", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":outbox_tray: Import a file", anchor=False)

topCol0, topCol1 = st.columns([0.75,0.25])
bottomCol0, bottomCol1, bottomCol2 = st.columns([0.3,0.4,0.3])

def uploadJsonFile(): #upload a file to display it in a dataset
    with bottomCol1:
        uploadedFile = st.file_uploader("Load a dataset file", type=['json', 'jsonl'], accept_multiple_files=False, help="Upload datasets in json / jsonl format",)
        if st.button(":outbox_tray: Load dataset"):
            if uploadedFile is not None:
                # Save the uploaded file temporarily
                temp_file_path = os.path.join(tempfile.gettempdir(), "temp_uploaded_file.json")
                with open(temp_file_path, "wb") as f:
                    f.write(uploadedFile.getbuffer())
                
                # Set the path in the session state
                st.session_state['temp_file_path'] = temp_file_path
                
                # Redirect to Edit page
                st.experimental_rerun()
            else:
                st.warning("You must choose a file to upload !")

uploadJsonFile()
