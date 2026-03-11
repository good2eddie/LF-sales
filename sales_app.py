import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(layout="wide")

FILE_NAME = "input_sayur_harian.xlsx"

st.title("Form Input Sayuran Harian")

tanggal = st.date_input("Tanggal", date.today())

# customer default
default_customers = [
    "Saigon",
    "Jittlada",
    "Aroya",
    "Sambal Dadakan",
    "Omah Badok",
    "Waterfall"
]

# sayuran
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
# Load data berdasarkan tanggal
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


existing_data = load_data_by_date(tanggal)

# =========================
# jika tidak ada data → default
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
# FORM INPUT
# =========================

st.subheader("Input Data")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

# =========================
# TOTAL PER SAYUR
# =========================

totals = edited_df[sayuran].sum()

total_row = {"customer": "TOTAL"}
for s in sayuran:
    total_row[s] = totals[s]

total_df = pd.DataFrame([total_row])

st.write("### Total")

st.dataframe(total_df, use_container_width=True)

st.divider()

# =========================
# SAVE DATA
# =========================

if st.button("Save"):

    edited_df["tanggal"] = tanggal

    cols = ["tanggal", "customer"] + sayuran
    edited_df = edited_df[cols]

    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)
        old["tanggal"] = pd.to_datetime(old["tanggal"]).dt.date

        old = old[old["tanggal"] != tanggal]

        new_df = pd.concat([old, edited_df], ignore_index=True)

    else:
        new_df = edited_df

    new_df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan")

# =========================
# TAMPIL DATA HARI INI
# =========================

st.subheader("Data Hari Ini")

if os.path.exists(FILE_NAME):

    df_all = pd.read_excel(FILE_NAME)

    df_all["tanggal"] = pd.to_datetime(df_all["tanggal"]).dt.date

    df_today = df_all[df_all["tanggal"] == tanggal]

    if df_today.empty:
        st.info("Data belum ada untuk tanggal ini")
    else:
        st.dataframe(
            df_today.drop(columns=["tanggal"]),
            use_container_width=True
        )

else:

    st.info("File Excel belum ada")
