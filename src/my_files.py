import pandas as pd
import streamlit as st
import os

# Función para guardar el archivo
def save_uploaded_file(uploaded_file):
    print("save_uploaded_file ..")
    print("uploaded_file : ",uploaded_file)
    if uploaded_file is not None:
        with open(os.path.join("data", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Archivo guardado: {}".format(uploaded_file.name))
    else:
        st.warning("Por favor, sube un archivo.")

# ---- READ EXCEL ----
@st.cache_data 
def get_data_from_excel(name):
    df = pd.read_excel(
        io=name,
        engine="openpyxl",
        sheet_name="Notas",
        #skiprows=3,
        #usecols="B:R",
        #nrows=1000,
    )
    # Add 'hour' column to dataframe
    return df


def upload_file_school(uploaded_file,storage):
    print(uploaded_file)
    print(type(uploaded_file))

    if uploaded_file != None:
        print("Saving original file")
        save_uploaded_file(uploaded_file)
        df = get_data_from_excel(uploaded_file)
        print("Saving prod")
        df.to_excel("prod.xlsx",index=False,sheet_name="Notas")
        
        storage.save(local_csv_file=os.path.join("data", uploaded_file.name),name=uploaded_file.name)
        storage.save(local_csv_file="prod.xlsx",name="prod.xlsx")