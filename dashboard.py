import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dasar
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
sns.set(style='darkgrid')

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("all_df.csv")

data = load_data()

# Sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Filter Data")
    
    # Filter Hari: Multiselect untuk memilih hari kerja dan/atau libur
    workingday_filter = st.multiselect("Pilih Hari", options=["Kerja", "Libur"], default=["Kerja", "Libur"])
    
    # Filter Variabel untuk Korelasi: Multiselect, defaultnya hanya memuat 'cnt'
    numeric_columns = data.select_dtypes(include='number').columns.tolist()
    selected_vars = st.multiselect("Pilih Variabel untuk Korelasi", options=numeric_columns, default=["cnt"])

# Filter data berdasarkan Hari
if "Kerja" in workingday_filter and "Libur" not in workingday_filter:
    filtered_data = data[data["workingday"] == 1]
elif "Libur" in workingday_filter and "Kerja" not in workingday_filter:
    filtered_data = data[data["workingday"] == 0]
else:
    filtered_data = data.copy()

# Pastikan kolom yang dipilih untuk korelasi ada di data numerik
numeric_data = filtered_data.select_dtypes(include='number')
selected_vars = [var for var in selected_vars if var in numeric_data.columns]

# Header
st.title("📊 Dashboard Penyewaan Sepeda")

# 1. Analisis Variabel yang Mempengaruhi Penyewaan Sepeda
st.header("1. Variabel yang Mempengaruhi Jumlah Penyewaan Sepeda")

if selected_vars:
    # Pastikan 'cnt' selalu ada untuk analisis korelasi
    if "cnt" not in selected_vars:
        selected_vars.append("cnt")
    
    corr = numeric_data[selected_vars].corr()
    st.subheader(f"Korelasi antara variabel terpilih dan 'cnt'")
    fig, ax = plt.subplots(figsize=(8, 6))
    # Tampilkan korelasi terhadap kolom 'cnt' diurutkan
    sns.heatmap(corr[['cnt']].sort_values(by='cnt', ascending=False), annot=True, cmap='YlGnBu', ax=ax)
    st.pyplot(fig)
    
    st.markdown("**Insight:** Variabel dengan korelasi tertinggi terhadap jumlah penyewaan sepeda memberikan indikasi faktor utama yang memengaruhi penyewaan.")
else:
    st.warning("Pilih minimal satu variabel untuk analisis korelasi.")

# 2. Perbedaan Penyewaan antara Hari Kerja dan Hari Libur
st.header("2. Perbedaan Penyewaan antara Hari Kerja dan Hari Libur")

# Gunakan data yang sudah difilter (filtered_data) agar sesuai dengan pilihan user
avg_rentals = filtered_data.groupby('workingday')['cnt'].mean().reset_index()

# Mapping: 0 = Libur, 1 = Kerja
avg_rentals['day_label'] = avg_rentals['workingday'].map({0: 'Libur', 1: 'Kerja'})

st.subheader("Rata-rata Penyewaan Sepeda")

fig, ax = plt.subplots()
# Tentukan urutan bar yang diinginkan: ['Libur', 'Kerja']
sns.barplot(
    x='day_label',
    y='cnt',
    data=avg_rentals,
    palette='Set2',
    order=['Libur', 'Kerja']  # agar bar "Libur" di kiri, "Kerja" di kanan
)

ax.set_xlabel("Hari")  # Ganti label sumbu X
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
st.pyplot(fig)

st.markdown("**Insight:** Grafik ini menunjukkan apakah terdapat perbedaan signifikan dalam jumlah penyewaan antara hari kerja dan hari libur.")

# Data yang Ditampilkan
st.markdown("### 📌 Data yang Ditampilkan")
st.dataframe(filtered_data)

st.caption("Dibuat oleh: Dicoding Student")
