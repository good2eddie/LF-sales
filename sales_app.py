import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(layout="wide")

FILE_NAME = "input_sayur_harian.xlsx"

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

# =========================
# Load data dari Excel
# =========================

def load_data_by_date(tanggal):

    if not os.path.exists(FILE_NAME):
        return None

    df = pd.read_excel(FILE_NAME)

    df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.date

    df_tgl = df[df["tanggal"] == tanggal]

    if df_tgl.empty:
        return None

    return df_tgl.drop(columns=["tanggal"])


# cek apakah ada data tanggal ini
existing_data = load_data_by_date(tanggal)

# =========================
# jika tidak ada data → pakai default
# =========================

if existing_data is None:

    data = []

    for cust in default_customers:
        row = {"customer": cust}
        for s in sayuran:
            row[s] = 0
        data.append(row)

    df = pd.DataFrame(data)

else:

    df = existing_data


# =========================
# Tabel Input
# =========================

st.subheader("Input Data")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

# =========================
# Save Data
# =========================

if st.button("Save"):

    edited_df["tanggal"] = tanggal

    cols = ["tanggal", "customer"] + sayuran
    edited_df = edited_df[cols]

    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)

        old["tanggal"] = pd.to_datetime(old["tanggal"]).dt.date

        # hapus data tanggal ini
        old = old[old["tanggal"] != tanggal]

        new_df = pd.concat([old, edited_df], ignore_index=True)

    else:

        new_df = edited_df

    new_df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan")
