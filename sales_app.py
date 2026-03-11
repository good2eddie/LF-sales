import streamlit as st
import pandas as pd
from datetime import date
import os

FILE_NAME = "input_sayur_harian.xlsx"

st.title("Form Input Sayuran Harian")

tanggal = st.date_input("Tanggal", date.today())

# daftar customer
default_customers = [
    "Sambal Dadakan",
    "Saigon",
    "Jittlada"
]

# daftar sayuran
sayuran = [
    "kangkung",
    "basil",
    "hot_basil",
    "selada",
    "ketumbar",
    "lobak",
    "daun_bawang_cung"
]

# buat dataframe awal
data = []

for cust in default_customers:
    row = {"customer": cust}
    for s in sayuran:
        row[s] = 0
    data.append(row)

df = pd.DataFrame(data)

st.write("### Input Data")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

st.write("---")

if st.button("Save to Excel"):

    edited_df["tanggal"] = tanggal

    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)
        new_df = pd.concat([old, edited_df], ignore_index=True)

    else:
        new_df = edited_df

    new_df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan ke Excel")
