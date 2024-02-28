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
# ---Open session--------------------
# ------------------------
df = st.session_state["df_data"]


# ------------------------
# ---Sidebar---------------------
# ------------------------
df = FoodDeliverySidebar.default_sidebar(df)

# ------------------------
# ---Layout Visão Entregador---------------------
# ------------------------

st.header("Food Dellivery")
st.subheader("Visão Entregador")

st.dataframe(df)

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
