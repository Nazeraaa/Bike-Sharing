import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style untuk seaborn
sns.set(style='whitegrid')

# Membaca dataset
df = pd.read_csv("data/hour.csv")

# Mengubah kolom 'dteday' menjadi tipe datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Fungsi untuk membuat DataFrame penyewaan harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample('D', on='dteday').sum().reset_index()
    daily_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    return daily_rentals_df

# Fungsi untuk membuat DataFrame penyewaan bulanan
def create_monthly_rentals_df(df):
    monthly_rentals_df = df.resample('M', on='dteday').sum().reset_index()
    monthly_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    return monthly_rentals_df

# Fungsi untuk membuat DataFrame penyewaan berdasarkan jam
def create_byhour_df(df):
    byhour_df = df.groupby('hr')['cnt'].sum().reset_index()
    byhour_df.rename(columns={"cnt": "total_customer"}, inplace=True)
    return byhour_df

# Fungsi untuk membuat DataFrame penyewaan berdasarkan musim
def create_byseasons_df(df):
    byseason_df = df.groupby('season')['cnt'].sum().reset_index()
    byseason_df.rename(columns={"cnt": "total_customer"}, inplace=True)
    return byseason_df

# Fungsi untuk membuat DataFrame penyewaan berdasarkan cuaca
def create_byweather_df(df):
    byweather_df = df.groupby('weathersit')['cnt'].sum().reset_index()
    byweather_df.rename(columns={"cnt": "total_customer"}, inplace=True)
    return byweather_df

# Fungsi untuk membuat clustering berdasarkan hari dan jam
def create_clustering(df):
    clustering = df.groupby(['weekday', 'hr'])['cnt'].sum().unstack()
    return clustering

# Mengurutkan data berdasarkan tanggal
df.sort_values(by='dteday', inplace=True)
df.reset_index(drop=True, inplace=True)

# Mendapatkan rentang tanggal
min_date = df['dteday'].min()
max_date = df['dteday'].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu yang dipilih
main_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Membuat DataFrame untuk berbagai analisis
byhour_df = create_byhour_df(main_df)
daily_rentals_df = create_daily_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df)
byseason_df = create_byseasons_df(main_df)
byweather_df = create_byweather_df(main_df)
clustering = create_clustering(main_df)

# Header dashboard
st.header('Bike Sharing Dashboard 🚀')

# Daily Rentals
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = daily_rentals_df['total_customer'].sum()
    st.metric("Total Rentals", value=total_rentals)
with col2:
    total_registered = daily_rentals_df['total_registered'].sum()
    st.metric("Total Registered Customer", value=total_registered)
with col3:
    total_casual = daily_rentals_df['total_casual'].sum()
    st.metric("Total Casual Customer", value=total_casual)

# Monthly Rentals
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(monthly_rentals_df['dteday'], monthly_rentals_df['total_customer'], marker='o', linewidth=2, color='skyblue')
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Total Customers", fontsize=15)
ax.set_title("Monthly Rentals (Total Customers)", fontsize=20)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)
st.pyplot(fig)

# Rental Patterns
st.subheader("Rental Patterns")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(y='total_customer', x='season', data=byseason_df.sort_values(by='total_customer', ascending=False), palette='viridis', ax=ax)
    ax.set_title("Customer based on Season", loc="center", fontsize=20, pad=20)
    ax.set_ylabel("Total Customers", fontsize=15)
    ax.set_xlabel("Season", fontsize=15)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(y='total_customer', x='weathersit', data=byweather_df.sort_values(by='total_customer', ascending=False), palette='viridis', ax=ax)
    ax.set_title("Customer based on Weather", loc="center", fontsize=20, pad=20)
    ax.set_ylabel("Total Customers", fontsize=15)
    ax.set_xlabel("Weather Situation", fontsize=15)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

# Customer based on Hour
st.subheader("Customer based on Hour")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='total_customer', data=byhour_df, marker='o', color='skyblue', ax=ax)
ax.set_title('Total Bike Rentals by Hour of the Day', fontsize=20)
ax.set_xlabel('Hour', fontsize=15)
ax.set_ylabel('Total Customers', fontsize=15)
ax.grid(axis='y')
st.pyplot(fig)


# Footer
st.caption('Copyright © muhammadichsanutama 2025')