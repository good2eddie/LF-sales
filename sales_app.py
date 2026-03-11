import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(layout="wide")

DATA_FOLDER = "data"
FILE_NAME = f"{DATA_FOLDER}/input_sayur_harian.xlsx"

st.title("Form Input Sayuran Harian")

tanggal = st.date_input("Tanggal", date.today())

# daftar customer
default_customers = [
    "Saigon",
    "Jittlada",
    "Aroya",
    "Sambal Dadakan",
    "Omah Badok",
    "Waterfall"
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

# pastikan folder data ada
os.makedirs(DATA_FOLDER, exist_ok=True)

# buat data awal tabel
data = []
for cust in default_customers:
    row = {"customer": cust}
    for s in sayuran:
        row[s] = 0
    data.append(row)

df = pd.DataFrame(data)

st.subheader("Input Data")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

if st.button("Save to Excel"):

    edited_df["tanggal"] = tanggal

    # urutan kolom
    cols = ["tanggal", "customer"] + sayuran
    edited_df = edited_df[cols]

    # jika file sudah ada
    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)

        # hapus data lama untuk tanggal yang sama
        old = old[old["tanggal"] != pd.to_datetime(tanggal)]

        new_df = pd.concat([old, edited_df], ignore_index=True)

    else:
        new_df = edited_df

    new_df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan")

    st.info(f"Total baris dalam file: {len(new_df)}")

# tampilkan data terakhir
if os.path.exists(FILE_NAME):

    st.subheader("Preview Data")

    preview = pd.read_excel(FILE_NAME)

    st.dataframe(
        preview.tail(20),
        use_container_width=True
    )
