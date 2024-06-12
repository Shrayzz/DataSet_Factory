import streamlit as st
import os
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSet Factory - Home", page_icon=":factory:", layout="wide", menu_items={"Get Help": 'https://github.com/Shrayzz/py_Jeu-de-Donnees/blob/main/README.md', "About": 'https://github.com/Shrayzz/py_Jeu-de-Donnees'})

st.title(":factory: DataSet Factory", anchor=False)

Col0, Col1, Col2 = st.columns([0.15,0.70,0.15])

def readFile(): # return the content of the README file
    with open('home.md', encoding="UTF-8") as md:
        content = md.read()
    return content

def markdownDisplay(text): # display text on the home page
    with Col1:
        with st.container(border=True):
                st.markdown(text)

markdownDisplay(readFile())
