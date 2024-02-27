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
    
    def clean_code(df1):
        """Feature Engiennier"""
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
        
        return df1
    
class CompanyVision:
    pass

class DeliverymanVision:
    pass

class RestaurantVision:
    def festival_AVG_STD(df1):
        df_aux = df1.loc[:,['Festival','Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['Time_taken_AVG','Time_taken_STD']
        df_aux = df_aux.reset_index()
        
        return df_aux