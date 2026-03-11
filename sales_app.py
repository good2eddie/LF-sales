import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(layout="wide")

FILE_NAME = "input_sayur_harian.xlsx"

st.title("Form Input Sayuran Harian")

tanggal = st.date_input("Tanggal", date.today())

# =========================
# daftar customer
# =========================

default_customers = [
    "Saigon",
    "Jittlada",
    "Aroya",
    "Sambal Dadakan",
    "Waterfall",
    "GMME Pd cabe",
    "Sadayana Sawangan",
    "Omah badok",
    "Pho Minh",
    "Gubuk Bamboe",
    "Madame Pho",
    "Rimbun Sunda",
    "Thai Sajja"    
]

# =========================
# daftar sayuran
# =========================

sayuran = [
    "Kangkung",
    "Basil",
    "Hot basil",
    "Selada",
    "Lobak",
    "D.Ketumbar",
    "DB cung"
]


# =========================
# convert input angka
# =========================

def convert_number(val):

    if pd.isna(val):
        return 0

    val = str(val).strip()

    if val == "":
        return 0

    val = val.replace(",", ".")

    try:
        return float(val)
    except:
        return 0


# =========================
# convert excel number → text
# =========================

def number_to_text(val):

    if pd.isna(val):
        return ""

    if isinstance(val, float) or isinstance(val, int):
        return str(val)

    return str(val)


# =========================
# load data berdasarkan tanggal
# =========================

def load_data_by_date(tanggal):

    if not os.path.exists(FILE_NAME):
        return None

    df = pd.read_excel(FILE_NAME)

    df["tanggal"] = pd.to_datetime(df["tanggal"]).dt.date

    df_tgl = df[df["tanggal"] == tanggal]

    if df_tgl.empty:
        return None

    df_tgl = df_tgl.drop(columns=["tanggal"])

    # ubah semua kolom sayur jadi TEXT
    for s in sayuran:
        df_tgl[s] = df_tgl[s].apply(number_to_text)

    return df_tgl


existing_data = load_data_by_date(tanggal)

# =========================
# default data
# =========================

if existing_data is None:

    data = []

    for cust in default_customers:

        row = {"customer": cust}

        for s in sayuran:
            row[s] = ""

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
# hitung total
# =========================

calc_df = edited_df.copy()

for s in sayuran:
    calc_df[s] = calc_df[s].apply(convert_number)

totals = calc_df[sayuran].sum()

total_row = {"customer": "TOTAL"}

for s in sayuran:
    total_row[s] = totals[s]

st.write("### Total")

st.dataframe(pd.DataFrame([total_row]), use_container_width=True)

st.divider()

# =========================
# SAVE DATA
# =========================

if st.button("Save"):

    save_df = calc_df.copy()

    save_df["tanggal"] = tanggal

    cols = ["tanggal", "customer"] + sayuran
    save_df = save_df[cols]

    if os.path.exists(FILE_NAME):

        old = pd.read_excel(FILE_NAME)

        old["tanggal"] = pd.to_datetime(old["tanggal"]).dt.date

        old = old[old["tanggal"] != tanggal]

        new_df = pd.concat([old, save_df], ignore_index=True)

    else:

        new_df = save_df

    new_df.to_excel(FILE_NAME, index=False)

    st.success("Data berhasil disimpan")


# =========================
# tampilkan data hari ini
# =========================

st.subheader("Data Hari Ini")

if os.path.exists(FILE_NAME):

    df_all = pd.read_excel(FILE_NAME)

    df_all["tanggal"] = pd.to_datetime(df_all["tanggal"]).dt.date

    df_today = df_all[df_all["tanggal"] == tanggal]

    if df_today.empty:

        st.info("Data belum ada")

    else:

        st.dataframe(
            df_today.drop(columns=["tanggal"]),
            use_container_width=True
        )

else:

    st.info("File Excel belum ada")
