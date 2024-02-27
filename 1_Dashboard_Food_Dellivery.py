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
from haversine import haversine


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
def import_dataset(path_row_file):
    if os.path.isfile(path_row_file):
        df_row = pd.read_csv(path_row_file)
    else:
        print('File ---{}--- not found'.format(path_row_file))
    return df_row
        
df = import_dataset("data/train.csv")


# ------------------------
# ---Feature Engiennier---------------------
# ------------------------
df1 = df.copy()

#01. Removed 'NaN' in columns 'Delivery_person_Age' end 'multiple_deliveries'
linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()
linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
df1= df1.loc[linhas_selecionadas, :].copy()

#2.C. Removendo espaço em branco no final do dado
df1['ID'] = df1['ID'].str.strip()
df1['Road_traffic_density'] = df1['Road_traffic_density'].str.strip()
df1['Type_of_order'] = df1['Type_of_order'].str.strip()
df1['Type_of_vehicle'] = df1['Type_of_vehicle'].str.strip()
df1['City'] = df1['City'].str.strip()
df1['Festival'] = df1['Festival'].str.strip()

#03. Removenco campos 'NaN' do DataSet
df1 = df1.loc[df1['Road_traffic_density'] != "NaN", :]
df1 = df1.loc[df1['City'] !='NaN', :]
df1 = df1.loc[df1['Road_traffic_density'] !='NaN', :]
df1 = df1.loc[df1['Festival'] != 'NaN', :]

#04. Limpando a coluna de time taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

#05 . Converter tipo de adequado
df1['Order_Date']= pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y') #erros = 'coercer'
df1['multiple_deliveries']= df1['multiple_deliveries'].astype(int)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
df1['Festival'] = df1['Festival'].map({'No': False, 'Yes': True})

#06. Criando a coluna de número da semana no ano
# mascara strftime: '%U' --> primeiro dia da semana domingo; '%W' --> primeiro dia da semana sendo segunda
df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')

#07. Criando a coluna da distância média dos resturantes e dos locais de entrega.
df1['delivery_distance_km'] = df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_longitude', 'Restaurant_latitude']].apply(lambda x: haversine(
            (x['Delivery_location_latitude'],x['Delivery_location_longitude']),
            (x['Restaurant_latitude'],x['Restaurant_longitude']),
    unit='km'), axis=1)

#08. Removendo "NaN"
df1 = df1.dropna(how="any", axis=0)

#09. Reindexação dos índices
df1 = df1.reset_index(drop=True)


# ------------------------
# ---Barra Lateral---------------------
# ------------------------

# ---
# ---Imagem de Logo
image_path = "images/boa-analise-de-dados.png"
image = Image.open (image_path)
st.sidebar.image(image, width=120)

# ---
# ---Input data 'min_order_date' end 'max_order_date'
min_order_date = df1['Order_Date'].min().to_pydatetime()
max_order_date = df1['Order_Date'].max().to_pydatetime()
order_data_filter = st.sidebar.slider(
    'Filtro Data', 
    min_value=min_order_date, 
    max_value=max_order_date, 
    value=[min_order_date, max_order_date]
)
# ---
# ---Input data 'Road_traffic_density'
road_traffic_values = df1['Road_traffic_density'].value_counts().index
road_traffics = st.sidebar.multiselect('Road_traffic_density', road_traffic_values, default=list(road_traffic_values))

# ---
# Filtro por 'Order_Date'
df1_filtered = (df1['Order_Date'] > order_data_filter[0]) & (df1['Order_Date'] < order_data_filter[1])
df1 = df1.loc[df1_filtered, :]
# ---
# Filtro por 'Road_traffic_density'
df1_filtered = df1['Road_traffic_density'].isin(road_traffics)
df1 = df1.loc[df1_filtered, :]


# ------------------------
# ---Layout Visão---------------------
# ------------------------
# st.header("Food Dellivery")
# st.subheader("Visão")

# # ---
# tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

# with tab1:
#     with st.container():
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Order by Day")
#             #Quantidade de entregas por cidade e por tipo de veículo
#             xpto = df1.loc[:, ['ID', 'City', 'Type_of_vehicle']].groupby( ['City','Type_of_vehicle']).count().reset_index()
#             st.dataframe(xpto, width=400)
#         with col2:
#             import numpy as np
#             st.bar_chart(np.random.randn(50, 3))
#     with st.container():
#         # Agrupamento
#         df_aux = df1.loc[:,['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
#         # Plotando gráfico de colunas
#         df_fig = px.bar(df_aux, x='Order_Date', y='ID')
#         # px.bar(df_aux, y='Order_Date', x='ID')
#         st.plotly_chart(df_fig, user_container_with=False)
#     with st.container():
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Traffic Order Share")
#             # Agrupamento
#             df_aux = df1.loc[:,['ID','Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
#             # Criando coluna de percentagem com o somatório dos pedidos por tráfego
#             df_aux['percentage_of_delivery'] = df_aux['ID']/df_aux['ID'].sum()
#             #plotando gráfico de pizza
#             df_fig = px.pie(df_aux, values='percentage_of_delivery', names='Road_traffic_density')
#             st.plotly_chart(df_fig, user_container_with=True)   
#         with col2:
#             st.subheader("Traffic Order City")
#             # Agrupamento
#             df_aux = df1.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
#             #plotando gráfico de pizza
#             df_fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
#             st.plotly_chart(df_fig, user_container_with=True)   
            
# #         st.write("This is inside the container")

# #         # You can call any Streamlit command, including custom components:
# #         import numpy as np
# #         st.bar_chart(np.random.randn(50, 3))      
        
# with tab2:
#     with st.container():
#         st.subheader("Order Share by Week")
#         # Quantidades de pedidos por semana "DIVIDIDO pelo" Número Ùnico de enteradores por semana
#         # Agrupamentos para a divisão
#         df_aux_01 = df1.loc[:,['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
#         df_aux_02 = df1.loc[:,['Delivery_person_ID','week_of_year']].groupby(['week_of_year']).nunique().reset_index()
#         # print(df_aux_01)
#         # print(df_aux_02)
#         # Junção dos DataFrames
#         df_aux = pd.merge(df_aux_01, df_aux_02, how='inner')
#         # print(df_aux)
#         # Criando coluna de quantidade de pedidos por entregador por semana
#         # df_aux['order_bu_deliver'] = df_aux.loc[:,'ID'] / df_aux.loc[:,'Delivery_person_ID']
#         df_aux['order_bu_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
#         # print(df_aux)
#         #plotando gráfico de pizza
#         df_fig = px.line(df_aux, x='week_of_year', y='order_bu_deliver')
#         st.plotly_chart(df_fig, user_container_with=True)
#     with st.container():
#         st.subheader("Order by Week")
#         # Agrupamento
#         df_aux = df1.loc[:,['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
#         #plotando gráfico de linhas
#         df_fig = px.line(df_aux, x='week_of_year', y='ID')
#         # px.bar(df_aux, x='week_of_year', y='ID')
#         st.plotly_chart(df_fig, user_container_with=True)
        
# with tab3:
#     st.header("tab3 em construção")
    
#     # # Médiana das lat e long --> valor central do conjunto de dados
#     df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
#     print(df_aux)
#     # # Instanciando objeto mapa com a biblioteca FOLIUM
#     map_mundi = folium.Map()


#     # # Inserindo valores
#     # folium.Marker([df_aux.loc[0,['Delivery_location_latitude']],
#     #                df_aux.loc[0,['Delivery_location_longitude']]],
#     #               popup=df_aux.loc[0,['City', 'Road_traffic_density']]).add_to(map_mundi)


#     # # Encapsulando coordenadas dentro do objeto interavel, um "DataFrame.iterrows"
#     for index, coordinate in df_aux.iterrows():
#         folium.Marker([coordinate['Delivery_location_latitude'],
#                        coordinate['Delivery_location_longitude']],
#                      popup=coordinate[['City', 'Road_traffic_density']]).add_to(map_mundi)
    
#     folium_static(map_mundi, width=1024, height=600)
    
# # ------------------------
# # ---Layout Visão Entregador---------------------
# # ------------------------
# st.header("Food Dellivery")
# st.subheader("Visão Entregador")

# # ---
# tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

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
        
        df_aux = df1.loc[:,['Festival','Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['Time_taken_AVG','Time_taken_STD']
        df_aux = df_aux.reset_index()
        
        with col1:
            total_entregadores = len(df1['Delivery_person_ID'].unique())
            st.metric('Quant Entregadores', total_entregadores)
        with col2:
            st.metric("Distáncia média", (np.round(df1['delivery_distance_km'].mean(),2)))
        with col3:
            st.metric("AVG com Festival", (np.round(df_aux.loc[df_aux['Festival'] == True, 'Time_taken_AVG'],2)))
        with col4:
            st.metric("AVG sem Festival", (np.round(df_aux.loc[df_aux['Festival'] == False, 'Time_taken_AVG'],2)))
        with col5:
            st.metric("STD com Festival", (np.round(df_aux.loc[df_aux['Festival'] == True, 'Time_taken_STD'],2)))
        with col6:
            st.metric("STD com Festival", (np.round(df_aux.loc[df_aux['Festival'] == False, 'Time_taken_STD'],2)))
    with st.container():
        avg_distance = df1.loc[:,['City','delivery_distance_km']].groupby('City').mean().reset_index()
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
        
        df_aux = df1.loc[:,['City','Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
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
