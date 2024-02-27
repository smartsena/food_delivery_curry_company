# ------------------------
# ---Imports---------------------
# ------------------------
import pandas as pd 
import numpy as np
import io 
import os

from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import folium
import streamlit as st
from streamlit_folium import folium_static
# from haversine import haversine
import utils


# ------------------------
# ---Page Config---------------------
# ------------------------
st.set_page_config(
    page_title="Food Dellivery",
    page_icon=":dart:",
    layout="wide"
)


# ------------------------
# ---Open session--------------------
# ------------------------
df = st.session_state["df_data"]


# ------------------------
# ---Barra Lateral---------------------
# ------------------------

# ---Input data 'min_order_date' end 'max_order_date'
# from datetime import datetime
min_order_date = df['Order_Date'].min().to_pydatetime()
max_order_date = df['Order_Date'].max().to_pydatetime()
order_data_filter = st.sidebar.slider(
    'Filtro Data', 
    min_value=min_order_date, 
    max_value=max_order_date, 
    value=[min_order_date, max_order_date]
)
# ---
# ---Input data 'Road_traffic_density'
road_traffic_values = df['Road_traffic_density'].value_counts().index
road_traffics = st.sidebar.multiselect('Road_traffic_density', road_traffic_values, default=list(road_traffic_values))

# ---
# Filtro por 'Order_Date'
df_filtered = (df['Order_Date'] > order_data_filter[0]) & (df['Order_Date'] < order_data_filter[1])
df = df.loc[df_filtered, :]
# ---
# Filtro por 'Road_traffic_density'
df_filtered = df['Road_traffic_density'].isin(road_traffics)
df = df.loc[df_filtered, :]

st.header("DataSet")
st.dataframe(df)


# ------------------------
# ---Layout Visão Entregador---------------------
# ------------------------

# ---
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '02', '03'])

with tab1:
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.subheader("Visão Entregador")
        with col2:
            st.subheader("Visão Entregador")
        with col3:
            st.subheader("Visão Entregador") 
        with col4:
            st.subheader("Visão Entregador") 
        with col5:
            st.subheader("Visão Entregador") 
        with col6:
            st.subheader("Visão Entregador")
    with st.container():
        st.subheader("Visão Entregador")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Visão Entregador")
        with col2:
            st.subheader("Visão Entregador")
    with st.container():
        st.subheader("Visão Entregador")
