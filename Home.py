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

# ------------------------
# ---Sidebar---------------------
# ------------------------
FoodDeliverySidebar.logo_sidebar()

st.sidebar.markdown("https://github.com/smartsena/FIFA_football_dashboard/")

# ------------------------
# ---Page---------------------
# ------------------------

st.header('🍲 :rainbow[FOOD DELIVERY CURRY COMPANY]')

st.link_button("Food Delivery Dataset","https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset/")
st.link_button("Portifólio de Projetos","https://smartsena.github.io/portifolio_projetos")

st.markdown("""
# FOOD DELIVERY CURRY COMPANY
CONTEXT
- This repository consists of analyzes and dashboards for the company's decision-making strategies.
""")
