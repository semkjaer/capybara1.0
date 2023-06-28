#  data imports
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# app imports
import uuid
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import json
import folium

from utils import auth, logo, get_data, plot
st.set_page_config(page_title='PinkCapybara', page_icon='favicon.ico', layout='wide', initial_sidebar_state='auto')
logo()

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"JPEG"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('application/src/background.JPEG') 

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

st.markdown('''
<style>
[data-testid="stHeader"] {
    display: none;
}
[data-baseweb="base-input"] {
    border:1px solid black; 
}
.streamlit-expander {
    background-color: #FFFFFF; 
}
[data-baseweb="select"] {
    margin-top: -40px;
    margin-bottom: -20px;
}
.block-container {
    padding-top: 0px !important;
    padding-right: 20px !important;
    padding-left: 20px !important;
    margin-top: -70px !important;
}
.streamlit-expanderContent {
    margin-top: -40px !important;
}
.row-widget .stButton {
    margin-top: 60px !important;
    margin-left: -40px !important;
}
[data-testid="stSidebarNav"] {  
    margin-bottom: 70px !important;
}
[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 225px !important;
    max-width: 225px !important;
}
</style>
''', unsafe_allow_html=True)

authenticator, config = auth()
with st.expander('Login', expanded=True):
    name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')

if os.path.exists('./data_combined.csv'):
         df = gpd.read_csv('./data_combined.csv')

gdf = get_data()

if st.session_state["authentication_status"]:
    with st.expander('', expanded=True):
        st.markdown('<p style="background-color:#FFFFFF;color:rgb(0, 71, 171);font-size:28px;border-radius:2%;">Jeugdzorg in kaart</p>', unsafe_allow_html=True)
        username = username.capitalize()
        col1, col2, _ = st.columns(3)
        if username in gdf.gm_naam.unique():
            with col1:
                option = st.selectbox("Selecteer gebied:", np.append([username], gdf.gm_naam.unique()[1:]))
        else:
            with col1:
                option = st.selectbox("", np.append(["Nederland"], gdf.gm_naam.unique()[1:]))
            if option == "Nederland":
                plot('NL00')
            else:
                with col2:
                    wijk = st.selectbox("", np.append(["Selecteer wijk (optioneel):"], gdf[(gdf.gm_naam == option) & (gdf.recs == 'Wijk')].regio.unique()))
                code = gdf[(gdf.gm_naam == option) & (gdf.recs == 'Gemeente')].gwb_code_10.unique()[0]
                if (wijk == "Selecteer wijk (optioneel):"):
                    plot(code)
                else:
                    plot(code)


elif authentication_status == False:
     st.error('Username/password is incorrect')