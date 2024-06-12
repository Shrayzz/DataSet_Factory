# DataSet Factory

## Introduction

DataSet_Factory is a Python application / tool who can read, edit, verify, export a dataset.

## How to install

### - Dependencies

Make sure you have one of latests versions of Python. Install all necessary packages with this command : `pip install streamlit pandas numpy`

## Usage

Run the app with `streamlit run .\src\Home.py`

### 1️ - Import a Dataframe

In the Import page you can import a Dataset in JSON or JSONL format, this is the dataset you will later work on.

### 2️ - Edit a Dataframe

In the Edit page here is the most important part. Here you can see your DatasSet as a DataFrame.
In this page you can:

- Change a Value
- Delete a Row
- Validate a Row
- Unvalidate a Row
- Validate All Row

### 3️ - Export Dataframe

In the Export page you can Export The Rows that have been verified to a DataSet. \
You have to choose the file name, in which folder you export it and in what type the DataSet will be (JSON, JSONL or Parquet)
