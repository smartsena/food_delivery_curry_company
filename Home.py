# streamlit run Dashboard_Food_Dellivery.py
# python Dashboard_Food_Dellivery.py


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
# ---Load DataSet--------------------
# ------------------------
if "df_data" not in st.session_state:  
    # ---Import---------------------
    df = utils.DataFrameRaw.import_dataset("data/train.csv")
    # ---Feature Engiennier---------------------
    df = utils.DataFrameRaw.clean_code(df)
    # ---Creat session---------------------
    st.session_state["df_data"] = df

df = st.session_state["df_data"]



    


st.markdown("""
# FOOD DELIVERY CURRY COMPANY
CONTEXT
- This repository consists of analyzes and dashboards for the company's decision-making strategies.""")
    
    
    
# st.plotly_char(fig)

# st.header(date_slider)


# ------------------------
# ------------------------
# ------------------------
# col1,col2 = st.columns(2)
# col3,col4,col5 = st.columns(3)

# fig_data = px.bar(df_filtered, x="dt_t_um", y="no_estagio", color="no_estagio", title="Data x Estágio")
# col1.plotly_chart(fig_data)


# fig_data2 = px.bar(df_filtered, x="dt_t_um", y="nu_area_ha", color="no_estagio", title="Data x Área total")
# col2.plotly_chart(fig_data2)


# stage_area = df_filtered.groupby("no_estagio")[["nu_area_ha"]].sum()
# stage_ti = df_filtered.groupby("no_estagio")[["nu_area_ha"]].count()
# st.sidebar.write(stage_area)
# st.sidebar.write(stage_ti)

# fig_data4 = px.bar(stage_area, title="Totais Área total x Estágio")
# col4.plotly_chart(fig_data4)

# # fig_data5 = px.pie(df_filtered, Values="stage", names="nu_area_ha", title="xpto")
# fig_data5 = px.pie(stage_area, title="xpto")
# col5.plotly_chart(fig_data5)

# df_filtered
# # btn_cmr2 = st.button("CMR-2")

# df