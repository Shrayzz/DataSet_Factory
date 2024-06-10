import streamlit as st
import os
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSet Factory - Export a file", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":outbox_tray: Export a DataSet", anchor=False)

# Colonnes pour la mise en page
topCol0, topCol1 = st.columns([0.75, 0.25])
bottomCol0, bottomCol1, bottomCol2 = st.columns([0.3, 0.4, 0.3])

# Fonction pour sauvegarder le DataFrame dans un fichier JSON, JSONL ou Parquet
def save_dataframe_to_file(df, directory, filename, file_format):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    if file_format.lower() == 'json':
        df.to_json(filepath, orient='records', lines=False)
    elif file_format.lower() == 'jsonl':
        df.to_json(filepath, orient='records', lines=True)
    elif file_format.lower() == 'parquet':
        df.to_parquet(filepath, engine='pyarrow', index=False)
    return filepath

# Charger le DataFrame depuis l'état de la session
if 'dataframe' in st.session_state:
    df = st.session_state['dataframe']
    
    st.text("Dataframe view :")
    st.dataframe(df, use_container_width=True, height=495)

    # Demander le nom du fichier à l'utilisateur
    file_name = st.text_input("Enter the file name (without extension):", value="exported_dataset")

    # Demander le répertoire de sauvegarde à l'utilisateur
    save_directory = st.text_input("Enter the directory where you want to save the file:", value="./datasets/exported", help="Default value corresponds to base destination folder you are")

    # Sélectionner le format de sauvegarde
    file_format = st.selectbox("Select file format to save:", ['JSON', 'JSONL', 'PARQUET'], help="For better reading, choose the extension which corresponds at dataframe selected")
    filename = f'{file_name}.{file_format.lower()}'
    
    # Bouton pour sauvegarder le DataFrame dans le format choisi
    if st.button("Save dataset"):
        try:
            filepath = save_dataframe_to_file(df, save_directory, filename, file_format)
            st.success(f"File saved successfully at {filepath}")
        except Exception as e:
            st.error(f"Error saving file: {e}")
else:
    st.warning(":warning: No dataset available to export. Please upload a dataset first.")
