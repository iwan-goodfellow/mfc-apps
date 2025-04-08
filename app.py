import streamlit as st
import pandas as pd
from datetime import date

CSV_FILE = 'penjualan-ayam.csv'

st.title("MFC ANALYTICAL FIN-APPS 🍗")

st.markdown('Masukkan data penjualan hari ini dan total pengeluaran')

# form buat input
with st.form('form penjualan'):
    tanggal = st.date_input('Tanggal', value=date.today())
    st.subheader('Jumlah Penjualan per Ayam')
    paha = st.number_input('Paha',min_value=0, step=1)
    dada = st.number_input('Dada',min_value=0, step=1)
    sayap = st.number_input('Sayap',min_value=0, step=1)
    lele = st.number_input('Lele',min_value=0, step=1)
    geprek = st.number_input('Geprek',min_value=0, step=1)

    st.subheader('Pengeluaran')
    pengeluaran = st.number_input('Total pengeluaran hari ini:', min_value=0, step=1000)
    submitted = st.form_submit_button('Simpan 📁')

# Harga per jenis ayam (edit sesuai usaha lo ya)
harga = {
    "paha": 8000,
    "dada": 9000,
    "sayap": 6000,
    "lele": 7000,
    "geprek": 12000
}

if submitted:
    pendapatan = (paha * harga['paha'] +
                  dada * harga['dada'] +
                  sayap * harga['sayap'] +
                  lele * harga['lele'] +
                  geprek * harga['geprek'])
    keuntungan = pendapatan - pengeluaran

    new_data = pd.DataFrame({
        "tanggal": [tanggal],
        "paha": [paha],
        "dada": [dada],
        "sayap": [sayap],
        "lele": [lele],
        "geprek": [geprek],
        "pendapatan": [pendapatan],
        "pengeluaran": [pengeluaran],
        "keuntungan bersih": [keuntungan]
    })

    try:
        existing = pd.read_csv(CSV_FILE)
        existing = existing[existing['tanggal'] != str(tanggal)]  # overwrite if tanggal already exists
        df = pd.concat([existing, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data

    df.to_csv(CSV_FILE, index=False)
    st.success(f"Data tanggal {tanggal} berhasil disimpan! ✅")

# ========== Edit / Hapus Data ==========
st.markdown("---")
st.header("✏️ Edit atau Hapus Data")

try:
    df = pd.read_csv(CSV_FILE, parse_dates=['tanggal'])
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    selected_date = st.selectbox("Pilih tanggal yang ingin diubah / hapus", df['tanggal'].dt.date.unique())
    row_to_edit = df[df['tanggal'].dt.date == selected_date].iloc[0]

    with st.form("form_edit"):
        st.write("Edit data tanggal:", selected_date)
        edit_paha = st.number_input("Paha", min_value=0, value=int(row_to_edit['paha']), step=1)
        edit_dada = st.number_input("Dada", min_value=0, value=int(row_to_edit['dada']), step=1)
        edit_sayap = st.number_input("Sayap", min_value=0, value=int(row_to_edit['sayap']), step=1)
        edit_lele = st.number_input("Lele", min_value=0, value=int(row_to_edit['lele']), step=1)
        edit_geprek = st.number_input("Geprek", min_value=0, value=int(row_to_edit['geprek']), step=1)
        edit_pengeluaran = st.number_input("Pengeluaran", min_value=0, value=int(row_to_edit['pengeluaran']), step=1000)
        simpan_edit = st.form_submit_button("Simpan Perubahan")
        hapus_data = st.form_submit_button("Hapus Data")

    if simpan_edit:
        df.loc[df['tanggal'].dt.date == selected_date, ['paha', 'dada', 'sayap', 'lele', 'geprek', 'pengeluaran']] = \
            [edit_paha, edit_dada, edit_sayap, edit_lele, edit_geprek, edit_pengeluaran]
        pendapatan = edit_paha * harga['paha'] + edit_dada * harga['dada'] + edit_sayap * harga['sayap'] + edit_lele * harga['lele'] + edit_geprek * harga['geprek']
        df.loc[df['tanggal'].dt.date == selected_date, 'pendapatan'] = pendapatan
        df.loc[df['tanggal'].dt.date == selected_date, 'keuntungan bersih'] = pendapatan - edit_pengeluaran
        df.to_csv(CSV_FILE, index=False)
        st.success("Data berhasil diperbarui!")

    elif hapus_data:
        df = df[df['tanggal'].dt.date != selected_date]
        df.to_csv(CSV_FILE, index=False)
        st.success("Data berhasil dihapus!")

except FileNotFoundError:
    st.info("Belum ada data yang bisa diedit atau dihapus.")
