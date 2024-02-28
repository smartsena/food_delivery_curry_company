# ------------------------
# ---Imports---------------------
# ------------------------
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import utils
from sidebar import FoodDeliverySidebar

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
# ---Sidebar---------------------
# ------------------------

df = FoodDeliverySidebar.default_sidebar(df)

# ------------------------
# ---Layout Visão Restaurante---------------------
# ------------------------
st.header("Food Dellivery")
st.subheader("Visão Restaurante")   

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