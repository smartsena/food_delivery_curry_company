import streamlit as st
from PIL import Image

class FoodDeliverySidebar:
    # def state_sidebar(df):
    #     # dff = df
    #     st.session_state["df_sidebar"] = df
    #     # del st.session_state["df_data"]
    #     return st.session_state["df_sidebar"]
    
    def logo_sidebar():
        # ---
        # ---Imagem de Logo
        image_path = "./images/images2.png"
        image = Image.open (image_path) # width=120)
        st.sidebar.image(image)
        st.sidebar.markdown("""---""")
        
    def default_sidebar(df):
        # ------------------------
        # ---Barra Lateral---------------------
        # ------------------------
        # ---
        
        # ---Create Session filtered with sidedar input values
        # if "df_sidebar" not in st.session_state:
        #     FoodDeliverySidebar.state_sidebar(df)
        # df = st.session_state["df_sidebar"]
        
        # ---
        # ---Imagem de Logo
        FoodDeliverySidebar.logo_sidebar()
        
        st.sidebar.subheader("DATASET FILTERS")
        # ---
        # ---Input data 'min_order_date' end 'max_order_date'
        # from datetime import datetime
        min_order_date = df['Order_Date'].min().to_pydatetime()
        max_order_date = df['Order_Date'].max().to_pydatetime()
        order_data_filter = st.sidebar.slider(
            'Data Filter', 
            min_value=min_order_date, 
            max_value=max_order_date, 
            value=[min_order_date, max_order_date]
        )
        st.sidebar.markdown("""---""")
        
        # ---
        # ---Input data 'Road_traffic_density'
        road_traffic_values = df['Road_traffic_density'].value_counts().index
        road_traffics = st.sidebar.multiselect('Traffic Density Filter', road_traffic_values, default=list(road_traffic_values))
        st.sidebar.markdown("""---""")
        
        # ---
        # Filtro por 'Order_Date'
        df_filtered = (df['Order_Date'] > order_data_filter[0]) & (df['Order_Date'] < order_data_filter[1])
        df = df.loc[df_filtered, :]
        
        # ---
        # Filtro por 'Road_traffic_density'
        df_filtered = df['Road_traffic_density'].isin(road_traffics)
        df = df.loc[df_filtered, :]

        return df
