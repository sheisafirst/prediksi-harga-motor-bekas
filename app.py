import streamlit as st
import pandas as pd
import joblib

# Membaca Dataset & Model
df = pd.read_csv("dataset_mofe.csv")
model = joblib.load("model_regresi_linear_motor_bekas.pkl")

st.set_page_config(page_title="Prediksi Harga Motor Bekas Honda")

st.title("🏍️ Prediksi Harga Sepeda Motor Bekas Honda")
st.write("Masukkan spesifikasi sepeda motor untuk memperoleh estimasi harga.")

# MERK & MODEL
merk_model = st.selectbox(
    "Merk & Model",
    sorted(df["Merk & Model"].dropna().unique())
)

# Filter berdasarkan merk
df_merk = df[df["Merk & Model"] == merk_model]

# TAHUN
tahun = st.number_input(
    "Tahun",
    min_value=int(df["Tahun"].min()),
    max_value=int(df["Tahun"].max()),
    value=int(df_merk["Tahun"].mode()[0])
)

# TIPE / VARIAN
varian_list = sorted(df_merk["Tipe / Varian"].dropna().unique())

tipe_varian = st.selectbox(
    "Tipe / Varian",
    varian_list
)

# Filter lagi berdasarkan varian
df_varian = df_merk[df_merk["Tipe / Varian"] == tipe_varian]

# JENIS TRANSMISI
jenis_transmisi = df_varian["Jenis Transmisi"].mode()[0]

if jenis_transmisi == "Cub":
    tampil_transmisi = "Motor Bebek (Cub)"
elif jenis_transmisi == "Sports":
    tampil_transmisi = "Motor Sport"
else:
    tampil_transmisi = "Matic"

st.text_input(
    "Jenis Transmisi",
    value=tampil_transmisi,
    disabled=True
)

# WARNA
warna = st.selectbox(
    "Warna",
    sorted(df_varian["Warna"].dropna().unique())
)

# JARAK TEMPUH
jarak_tempuh = st.number_input(
    "Jarak Tempuh (KM)",
    min_value=0,
    value=10000,
    step=1000
)

# STNK
stnk = st.selectbox(
    "STNK",
    sorted(df["STNK"].dropna().unique())
)

# BPKB
bpkb = st.selectbox(
    "BPKB",
    sorted(df["BPKB"].dropna().unique())
)

# BUKU SERVIS
buku_servis = st.selectbox(
    "Buku Servis",
    sorted(df["Buku Servis"].dropna().unique())
)

# PREDIKSI
if st.button("Prediksi Harga"):

    data_baru = pd.DataFrame({

        "Merk & Model": [merk_model],
        "Tahun": [tahun],
        "Tipe / Varian": [tipe_varian],
        "Jenis Transmisi": [jenis_transmisi],
        "Warna": [warna],
        "Jarak Tempuh": [jarak_tempuh],
        "STNK": [stnk],
        "BPKB": [bpkb],
        "Buku Servis": [buku_servis]

    })

    hasil = model.predict(data_baru)[0]

    st.success(f"Estimasi Harga Motor Bekas: Rp {hasil:,.0f}")