import streamlit as st
import os
import pandas as pd
import numpy as np
import db

st.set_page_config(page_title="DataSet Factory - Export a file", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":outbox_tray: Export a DataSet", anchor=False)

# Colonnes pour la mise en page
topCol0, topCol1 = st.columns([0.75, 0.25])
bottomCol0, bottomCol1, bottomCol2 = st.columns([0.3, 0.4, 0.3])

uploadedFile = st.session_state.get('uploadedFile', None)

# Fonction pour sauvegarder le DataFrame dans un fichier JSON, JSONL ou Parquet
def save_dataframe_to_file(df, directory, filename, file_format):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    if file_format.lower() == 'json':
        df.to_json(filepath, orient='records', lines=False, indent=True)
    elif file_format.lower() == 'jsonl':
        df.to_json(filepath, orient='records', lines=True)
    elif file_format.lower() == 'parquet':
        df.to_parquet(filepath, engine='pyarrow', index=False)
    return filepath

# Charger le DataFrame depuis l'état de la session
try:
    tableName = uploadedFile.name.replace("-", "_").split('.',1)[0]
    df = db.GetDfFromDb(tableName, f"SELECT * FROM {tableName} WHERE isValidate = 1")
    df = df.drop(columns=['isValidate'])

    st.header(f":heavy_check_mark: DataSet validated ({db.CountValidatedRow(tableName)} row(s)) :")

    if (df.empty):
        st.warning("No rows have been validated yet !")
    else:
        st.dataframe(df, hide_index=True, use_container_width=True, height=495)

    # Demander le nom du fichier à l'utilisateur
    file_name = st.text_input("Enter the file name (without extension):", value="exported_dataset")

    # Demander le répertoire de sauvegarde à l'utilisateur
    save_directory = st.text_input("Enter the directory where you want to save the file:", value=".\datasets\exported", help="Default value corresponds to base destination folder you are")

    # Sélectionner le format de sauvegarde
    file_format = st.selectbox("Select file format to save:", ['JSON', 'JSONL', 'PARQUET'], help="For better reading, choose the extension which corresponds at dataframe selected")
    filename = f'{file_name}.{file_format.lower()}'
    
    # Bouton pour sauvegarder le DataFrame dans le format choisi
    if st.button("Save dataset"):
        if (not df.empty):
            filepath = save_dataframe_to_file(df, save_directory, filename, file_format)
            st.success(f":heavy_check_mark: File saved successfully at {filepath}")
        else:
            st.error("Can't export DataSet, no rows have been validated !")
except:
    st.warning(":warning: No dataset available to export. Please upload a dataset first.")
