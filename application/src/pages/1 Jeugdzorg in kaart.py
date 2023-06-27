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
import folium

from utils import auth, logo, get_data, plot
st.set_page_config(page_title='PinkCapybara', page_icon = 'favicon.ico', layout = 'wide', initial_sidebar_state = 'auto')
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
    with st.expander('Home page', expanded=True):
        st.title("Jeugdzorg in kaart")
        st.write("Hier kan je kaarten bekijken")
        username = username.capitalize()
        if username in gdf.gm_naam.unique():
            option = st.selectbox("Selecteer gebied:", np.append([username], gdf.gm_naam.unique()[1:]))
        else:
            option = st.selectbox("", np.append(["Nederland"], gdf.gm_naam.unique()[1:]))
            if option == "Nederland":
                st.image('./map.png')
            else:
                code = gdf[(gdf.gm_naam == option) & (gdf.recs == 'Gemeente')].gwb_code_10.unique()[0]
                plot(code)

elif authentication_status == False:
     st.error('Username/password is incorrect')