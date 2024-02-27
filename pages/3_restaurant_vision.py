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


# ------------------------
# ---Layout Visão Restaurante---------------------
# ------------------------
st.header("Food Dellivery")
st.subheader("Visão Restaurante")    
  
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.subheader("Analisando as entregas")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        df_aux = utils.RestaurantVision.festival_AVG_STD(df)# df_aux.reset_index()
        
        with col1:
            total_entregadores = len(df['Delivery_person_ID'].unique())
            st.metric('Quant Entregadores', total_entregadores)
        with col2:
            st.metric("Distáncia média", (np.round(df['delivery_distance_km'].mean(),2)))
        with col3:
            st.metric("AVG com Festival", (np.round(df_aux.loc[df_aux['Festival'] == True, 'Time_taken_AVG'],2)))
        with col4:
            st.metric("AVG sem Festival", (np.round(df_aux.loc[df_aux['Festival'] == False, 'Time_taken_AVG'],2)))
        with col5:
            st.metric("STD com Festival", (np.round(df_aux.loc[df_aux['Festival'] == True, 'Time_taken_STD'],2)))
        with col6:
            st.metric("STD com Festival", (np.round(df_aux.loc[df_aux['Festival'] == False, 'Time_taken_STD'],2)))
    with st.container():
        avg_distance = df.loc[:,['City','delivery_distance_km']].groupby('City').mean().reset_index()
        df_fig = go.Figure(
            data=[go.Pie(labels=avg_distance['City'], values=avg_distance['delivery_distance_km'], pull=[0, 0.1,0])]
        )
        st.plotly_chart(df_fig)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Visão Restaurante")
        with col2:
            st.subheader("Visão Restaurante")
    with st.container():
        st.subheader("Visão Restaurante")
        
        df_aux = df.loc[:,['City','Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['Time_taken_AVG','Time_taken_STD']
        df_aux = df_aux.reset_index()
        

        #Criando gráfico de SUMBURST
        df_fig = px.sunburst(df_aux, 
                             path=['City','Road_traffic_density'],
                             values='Time_taken_AVG',
                             color='Time_taken_STD',
                             color_continuous_scale='RdBu',
                             color_continuous_midpoint=np.average(df_aux['Time_taken_STD']))
        # Plotando gráfico
        st.plotly_chart(df_fig)
        st.dataframe(df_aux)
# ---  