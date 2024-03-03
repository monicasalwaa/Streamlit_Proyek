


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_byprice_df(df):
  byprice_df = df.groupby(by="product_category_name").price.sum().reset_index()
  byprice_df.rename(columns={
    "price": "top_price"
}, inplace=True)

  return byprice_df

def create_bystate_df(df):
  bystate_df = df.groupby(by="customer_state").order_id.nunique().reset_index()
  bystate_df.rename(columns={
    "order_id": "customer_count"
}, inplace=True)

  return bystate_df

def create_byproduct_df(df):
  byproduct_df = df.groupby(by="product_category_name").order_id.nunique().reset_index()
  byproduct_df.rename(columns={
    "order_id": "order_count"
}, inplace=True)

  return byproduct_df

def create_rfm_df(df):
    rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
      "order_purchase_timestamp": "max", # mengambil tanggal order terakhir
      "order_id": "nunique", # menghitung jumlah order
      "price": "sum" # menghitung jumlah revenue yang dihasilkan
    })
    rfm_df.columns = ["customer_id","max_order_purchase_timestamp", "frequency", "monetary"]

    rfm_df["max_order_purchase_timestamp"] = pd.to_datetime(rfm_df["max_order_purchase_timestamp"])
    recent_date = all_df["order_purchase_timestamp"].max()
    rfm_df["recency"] = (recent_date - rfm_df["max_order_purchase_timestamp"]).dt.days

    rfm_df.drop("max_order_purchase_timestamp", axis=1, inplace=True)

    return rfm_df

all_df=pd.read_csv("https://raw.githubusercontent.com/monicasalwaa/Proyek_Akhir/main/dashboard/all_data.csv")

datetime_columns = ["shipping_limit_date", "order_purchase_timestamp",	"order_approved_at",	"order_delivered_carrier_date", "order_delivered_customer_date",	"order_estimated_delivery_date"]

for column in datetime_columns:
  all_df[column] = pd.to_datetime(all_df[column])

all_df["order_estimated_delivery_date"] = pd.to_datetime(all_df["order_estimated_delivery_date"])


#Membuat Komponen Filter:

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("toko_online.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
byprice_df = create_byprice_df(main_df)
bystate_df = create_bystate_df(main_df)
byproduct_df = create_byproduct_df(main_df)
rfm_df = create_rfm_df(main_df)


# plot number of daily orders (2021)
st.header(':sparkles: All You Need Store Dashboard :sparkles:')

st.subheader('Top Price Products in All You Need Store')


fig = plt.figure(figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="top_price", y="product_category_name", data=byprice_df.sort_values(by="top_price", ascending=False).head(10),
    palette=colors
)
plt.title("Top 10 Expensive Product Categories", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Customer Demographics')

fig = plt.figure(figsize=(35, 15))
colors_ = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="customer_count", y="customer_state", data=bystate_df.sort_values(by="customer_count", ascending=False).head(10),
    palette=colors_
)
plt.title("Number of Customer by States", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
plt.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Top Product Categories by Number of Sale')

fig = plt.figure(figsize=(35, 15))
colors_ = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="order_count", y="product_category_name", data=byproduct_df.sort_values(by="order_count", ascending=False).head(10),
    palette=colors_
)
plt.title("Top 10 Product by Number of Sales", loc="center", fontsize=50)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
plt.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Best Customer Based on RFM Parameters')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO')
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)



