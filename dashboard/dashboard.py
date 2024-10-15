import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/all_data.csv')  # Sesuaikan path file sesuai kebutuhan
    return data

data = load_data()

# Pemetaan musim dan cuaca (jika belum ada)
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain"}

# Menambahkan kolom deskriptif untuk musim dan cuaca
data['season_name'] = data['season'].map(season_mapping)
data['weather_name'] = data['weathersit'].map(weather_mapping)

# Judul Dashboard
st.title("Bike Sharing Dashboard")

# Sidebar
st.sidebar.header("Filters")
season_options = data['season_name'].unique()
selected_seasons = st.sidebar.multiselect("Select Seasons", options=season_options, default=season_options.tolist())
working_days = st.sidebar.checkbox("Show Only Working Days", value=False)

# Filter data berdasarkan input dari pengguna
filtered_data = data[data['season_name'].isin(selected_seasons)]
if working_days:
    filtered_data = filtered_data[filtered_data['workingday'] == 1]

# Tampilkan ringkasan data
if st.checkbox("Show Data Summary"):
    st.write(filtered_data.describe())

# Menampilkan total penyewaan
total_rentals = filtered_data['cnt'].sum()
st.metric(label="Total Rentals", value=total_rentals)

# Menambahkan tab untuk visualisasi
tab1, tab2, tab3, tab4 = st.tabs(["Musim vs Penyewaan", "Hari Kerja", "Suhu vs Penyewaan", "Cuaca vs Penyewaan"])

# Tab 1: Musim vs Penyewaan
with tab1:
    st.subheader("Pengaruh Musim Terhadap Jumlah Penyewaan")
    fig_season = px.box(filtered_data, x='season_name', y='cnt', title="Jumlah Penyewaan Berdasarkan Musim")
    st.plotly_chart(fig_season)

# Tab 2: Hari Kerja
with tab2:
    st.subheader("Pengaruh Hari Kerja Terhadap Jumlah Penyewaan")
    fig_working_day = px.bar(
        filtered_data.groupby('workingday')['cnt'].sum().reset_index(),
        x='workingday',
        y='cnt',
        title="Jumlah Penyewaan Berdasarkan Hari Kerja",
        labels={'workingday': 'Hari Kerja (0 = Tidak, 1 = Ya)', 'cnt': 'Jumlah Penyewaan'}
    )
    st.plotly_chart(fig_working_day)

# Tab 3: Suhu vs Penyewaan
with tab3:
    st.subheader("Hubungan Antara Suhu dan Jumlah Penyewaan di Hari Non-libur")
    non_holiday_data = filtered_data[filtered_data['holiday'] == 0]
    fig_temp = px.scatter(non_holiday_data, x='temp', y='cnt', title="Suhu vs Jumlah Penyewaan (Non-libur)", trendline="ols")
    st.plotly_chart(fig_temp)


# Tab 4: Cuaca vs Penyewaan (Bar Chart)
with tab4:
    st.subheader("Pengaruh Cuaca Terhadap Jumlah Penyewaan")
    
    # Menggunakan Plotly untuk Bar Chart
    fig_weather = px.bar(filtered_data, x='weather_name', y='cnt', title="Jumlah Penyewaan Berdasarkan Cuaca", 
                         labels={'weather_name': 'Cuaca', 'cnt': 'Jumlah Penyewaan'}, 
                         color='weather_name',
                         height=500)
    st.plotly_chart(fig_weather)
