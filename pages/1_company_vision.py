# ------------------------
# ---Imports---------------------
# ------------------------
import pandas as pd 
# import numpy as np
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
from sidebar import FoodDeliverySidebar
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
df = utils.DataFrameRaw.user_session_state()

# ------------------------
# ---Sidebar---------------------
# ------------------------
df = FoodDeliverySidebar.default_sidebar(df)

# ------------------------
# ---Layout Visão---------------------
# ------------------------
st.header("Food Dellivery")
st.subheader("Visão Empresa")

# ---
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    # with st.container():
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.subheader("Order by Day")
    #         #Quantidade de entregas por cidade e por tipo de veículo
    #         xpto = df.loc[:, ['ID', 'City', 'Type_of_vehicle']].groupby( ['City','Type_of_vehicle']).count().reset_index()
    #         st.dataframe(xpto, width=400)
    #     with col2:
    #         import numpy as np
    #         st.bar_chart(np.random.randn(50, 3))
    with st.container():
        # Agrupamento
        df_aux = df.loc[:,['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
        # Plotando gráfico de colunas
        df_fig = px.bar(df_aux, x='Order_Date', y='ID')
        # px.bar(df_aux, y='Order_Date', x='ID')
        st.plotly_chart(df_fig, user_container_with=False)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Traffic Order Share")
            # Agrupamento
            df_aux = df.loc[:,['ID','Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
            # Criando coluna de percentagem com o somatório dos pedidos por tráfego
            df_aux['percentage_of_delivery'] = df_aux['ID']/df_aux['ID'].sum()
            #plotando gráfico de pizza
            df_fig = px.pie(df_aux, values='percentage_of_delivery', names='Road_traffic_density')
            st.plotly_chart(df_fig, user_container_with=True)   
        with col2:
            st.subheader("Traffic Order City")
            # Agrupamento
            df_aux = df.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
            #plotando gráfico de pizza
            df_fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            st.plotly_chart(df_fig, user_container_with=True)   
            
#         st.write("This is inside the container")

#         # You can call any Streamlit command, including custom components:
#         import numpy as np
#         st.bar_chart(np.random.randn(50, 3))      
        
with tab2:
    with st.container():
        st.subheader("Order Share by Week")
        # Quantidades de pedidos por semana "DIVIDIDO pelo" Número Ùnico de enteradores por semana
        # Agrupamentos para a divisão
        df_aux_01 = df.loc[:,['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
        df_aux_02 = df.loc[:,['Delivery_person_ID','week_of_year']].groupby(['week_of_year']).nunique().reset_index()
        # print(df_aux_01)
        # print(df_aux_02)
        # Junção dos DataFrames
        df_aux = pd.merge(df_aux_01, df_aux_02, how='inner')
        # print(df_aux)
        # Criando coluna de quantidade de pedidos por entregador por semana
        # df_aux['order_bu_deliver'] = df_aux.loc[:,'ID'] / df_aux.loc[:,'Delivery_person_ID']
        df_aux['order_bu_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        # print(df_aux)
        #plotando gráfico de pizza
        df_fig = px.line(df_aux, x='week_of_year', y='order_bu_deliver')
        st.plotly_chart(df_fig, user_container_with=True)
    with st.container():
        st.subheader("Order by Week")
        # Agrupamento
        df_aux = df.loc[:,['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
        #plotando gráfico de linhas
        df_fig = px.line(df_aux, x='week_of_year', y='ID')
        # px.bar(df_aux, x='week_of_year', y='ID')
        st.plotly_chart(df_fig, user_container_with=True)
        
with tab3:
    st.header("tab3 em construção")
    
    # # Médiana das lat e long --> valor central do conjunto de dados
    df_aux = df.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    # # Instanciando objeto mapa com a biblioteca FOLIUM
    map_mundi = folium.Map()


    # # Inserindo valores
    # folium.Marker([df_aux.loc[0,['Delivery_location_latitude']],
    #                df_aux.loc[0,['Delivery_location_longitude']]],
    #               popup=df_aux.loc[0,['City', 'Road_traffic_density']]).add_to(map_mundi)


    # # Encapsulando coordenadas dentro do objeto interavel, um "DataFrame.iterrows"
    for index, coordinate in df_aux.iterrows():
        folium.Marker([coordinate['Delivery_location_latitude'],
                       coordinate['Delivery_location_longitude']],
                     popup=coordinate[['City', 'Road_traffic_density']]).add_to(map_mundi)
    
    folium_static(map_mundi, width=1024, height=600)