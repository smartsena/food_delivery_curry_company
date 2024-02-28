import pandas as pd 
# import numpy as np
# import io 
import os
from haversine import haversine

        
class DataFrameRaw:
    def import_dataset(path_raw_file):
        """Load DataSet"""
        if os.path.isfile(path_raw_file):
            df_raw = pd.read_csv(path_raw_file)
        else:
            print('File ---{}--- not found'.format(path_raw_file))
        return df_raw
    
    def clean_code(df):
        """Feature Engiennier"""
        #01. Removed 'NaN' in columns 'Delivery_person_Age' end 'multiple_deliveries'
        linhas_selecionadas = df['Delivery_person_Age'] != 'NaN '
        df = df.loc[linhas_selecionadas, :].copy()
        linhas_selecionadas = df['multiple_deliveries'] != 'NaN '
        df= df.loc[linhas_selecionadas, :].copy()

        #2.C. Removendo espaço em branco no final do dado
        df['ID'] = df['ID'].str.strip()
        df['Road_traffic_density'] = df['Road_traffic_density'].str.strip()
        df['Type_of_order'] = df['Type_of_order'].str.strip()
        df['Type_of_vehicle'] = df['Type_of_vehicle'].str.strip()
        df['City'] = df['City'].str.strip()
        df['Festival'] = df['Festival'].str.strip()

        #03. Removenco campos 'NaN' do DataSet
        df = df.loc[df['Road_traffic_density'] != "NaN", :]
        df = df.loc[df['City'] !='NaN', :]
        df = df.loc[df['Road_traffic_density'] !='NaN', :]
        df = df.loc[df['Festival'] != 'NaN', :]

        #04. Limpando a coluna de time taken
        df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
        df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)

        #05 . Converter tipo de adequado
        df['Order_Date']= pd.to_datetime(df['Order_Date'], format='%d-%m-%Y') #erros = 'coercer'
        df['multiple_deliveries']= df['multiple_deliveries'].astype(int)
        df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)
        df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)
        df['Festival'] = df['Festival'].map({'No': False, 'Yes': True})

        #06. Criando a coluna de número da semana no ano
        # mascara strftime: '%U' --> primeiro dia da semana domingo; '%W' --> primeiro dia da semana sendo segunda
        df['week_of_year'] = df['Order_Date'].dt.strftime('%U')

        #07. Criando a coluna da distância média dos resturantes e dos locais de entrega.
        df['delivery_distance_km'] = df.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_longitude', 'Restaurant_latitude']].apply(lambda x: haversine(
                    (x['Delivery_location_latitude'],x['Delivery_location_longitude']),
                    (x['Restaurant_latitude'],x['Restaurant_longitude']),
            unit='km'), axis=1)

        #08. Removendo "NaN"
        df = df.dropna(how="any", axis=0)

        #09. Reindexação dos índices
        df = df.reset_index(drop=True)
        
        return df
    
class CompanyVision:
    pass

class DeliverymanVision:
    pass

class RestaurantVision:
    def festival_AVG_STD(df):
        df_aux = (df.loc[:,['Festival','Time_taken(min)']].
                  groupby('Festival').
                  agg({'Time_taken(min)': ['mean','std']}))
        df_aux.columns = ['Time_taken_AVG','Time_taken_STD']
        df_aux = df_aux.reset_index()
        
        return df_aux