# ------------------------
# ---Imports---------------------
# ------------------------
import pandas as pd 
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
df = utils.DataFrameRaw.user_session_state()

# ------------------------
# ---Sidebar---------------------
# ------------------------
df = FoodDeliverySidebar.default_sidebar(df)

# ------------------------
# ---Layout Visão Entregador---------------------
# ------------------------

st.header("Food Dellivery")
st.subheader("Visão Entregador")

st.dataframe(df,column_config={
    'Delivery_person_Ratings':st.column_config.ProgressColumn(
        "Delivery_person_Ratings",
        min_value=0,
        max_value=df['Delivery_person_Ratings'].max(),
        format=" %f",),})
st.write("...page under construction")

# ---
# tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '02', '03'])

# with tab1:
#     with st.container():
#         col1, col2, col3, col4, col5, col6 = st.columns(6)
#         with col1:
#             st.subheader("Visão Entregador")
#         with col2:
#             st.subheader("Visão Entregador")
#         with col3:
#             st.subheader("Visão Entregador") 
#         with col4:
#             st.subheader("Visão Entregador") 
#         with col5:
#             st.subheader("Visão Entregador") 
#         with col6:
#             st.subheader("Visão Entregador")
#     with st.container():
#         st.subheader("Visão Entregador")
#     with st.container():
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Visão Entregador")
#         with col2:
#             st.subheader("Visão Entregador")
#     with st.container():
#         st.subheader("Visão Entregador")
