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

from utils import auth, logo, get_data

logo()

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator, config = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')

# if os.path.exists('./data_combined.csv'):
#          df = gpd.read_csv('./data_combined.csv')

# df = get_data()
# gdf = gpd.GeoDataFrame(df, crs="EPSG:28992", geometry=df.geometry)
# fig, ax = plt.subplots(figsize = (12,12))
# gdf.plot(ax=ax, column="AANT_INW",legend=True, legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"})

if st.session_state["authentication_status"]:
    st.title("Jeugdzorg in kaart")
    st.write("This is the model page.")
    # st.pyplot(fig)
elif authentication_status == False:
     st.error('Username/password is incorrect')

