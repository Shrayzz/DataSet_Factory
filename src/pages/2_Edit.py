import streamlit as st
import os
import pandas as pd
import numpy as np
import db

st.set_page_config(page_title="DataSet Factory - Edit a DataSet", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":pencil: Edit a DataSet", anchor=False)

topCol0, topCol1 = st.columns([0.75,0.25])

# Load the temporary file path from session state
temp_file_path = st.session_state.get('temp_file_path', None)
if temp_file_path and os.path.exists(temp_file_path):
    df = pd.read_json(temp_file_path)
    
    # Clean the dataframe to remove any null characters
    df = df.applymap(lambda x: x.replace('\x00', '') if isinstance(x, str) else x)
    
    with topCol0:
        st.header(":pushpin: Uploaded Dataset")
        st.dataframe(db.CreateDB(df), use_container_width=True, height=495)
        
    with topCol1:
        st.header(":clipboard: Informations")
        with st.container():
            st.write("Rows: ", df.shape[0])
            st.write("Columns: ", df.shape[1])
            st.write("Columns Names: ", df.columns.tolist())
            st.write("Columns Unique Values: ", df.nunique())
    
    # Optionally remove the temporary file after reading
    # os.remove(temp_file_path)
else:
    st.warning("No dataset loaded. Please upload a dataset in the Import section.")
