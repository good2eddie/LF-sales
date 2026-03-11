import streamlit as st
import pandas as pd
from datetime import date
import os

FILE_NAME = "input_sayur_harian.xlsx"

# daftar customer default
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

st.title("Form Input Sayuran Harian")

tanggal = st.date_input("Tanggal", date.today())

st.write("### Input Data")

data = []

for i, cust in enumerate(default_customers):

    col = st.columns(len(sayuran) + 1)

    customer = col[0].text_input(
        f"Customer {i+1}",
        value=cust,
        key=f"cust{i}"
    )

    row = {
        "tanggal": tanggal,
        "customer": customer
    }

    for j, sayur in enumerate(sayuran):

        val = col[j+1].number_input(
            sayur,
            min_value=0.0,
            step=0.1,
            key=f"{sayur}{i}"
        )

        row[sayur] = val

    data.append(row)

st.write("---")

if st.button("Save to Excel"):

    df = pd.DataFrame(data)

    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)

        df = pd.concat([old, df], ignore_index=True)

    df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan ke Excel")
