import streamlit as st
import pandas as pd

CSV_FILE = 'penjualan-ayam.csv'

st.title("📈 Laporan Penjualan Ayam")

try:
    df = pd.read_csv(CSV_FILE, parse_dates=['tanggal'])
    df['tanggal'] = pd.to_datetime(df['tanggal'])
except FileNotFoundError:
    st.warning("Belum ada data penjualan.")
    st.stop()

# Cek duplikat
duplikat = df[df.duplicated(subset='tanggal', keep=False)]
if not duplikat.empty:
    st.error("⚠️ Terdapat data dengan tanggal yang dobel:")
    st.dataframe(duplikat)

# Ringkasan Mingguan
st.subheader("🗓️ Ringkasan Mingguan")
df['minggu'] = df['tanggal'].dt.to_period('W').astype(str)
weekly = df.groupby('minggu')[['pendapatan', 'pengeluaran', 'keuntungan bersih']].sum()
st.dataframe(weekly)

# Ringkasan Bulanan
st.subheader("📅 Ringkasan Bulanan")
df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)
monthly = df.groupby('bulan')[['pendapatan', 'pengeluaran', 'keuntungan bersih']].sum()
st.dataframe(monthly)

# Ringkasan Tahunan
st.subheader("📆 Ringkasan Tahunan")
df['tahun'] = df['tanggal'].dt.year
yearly = df.groupby('tahun')[['pendapatan', 'pengeluaran', 'keuntungan bersih']].sum()
st.dataframe(yearly)

# Grafik Tren Keuntungan
st.subheader("📊 Grafik Keuntungan Harian")
st.line_chart(df.set_index('tanggal')['keuntungan bersih'])
