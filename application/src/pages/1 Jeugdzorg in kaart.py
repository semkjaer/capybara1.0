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
import folium

from utils import auth, logo, get_data
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
# gdf = gpd.GeoDataFrame(df, crs="EPSG:28992", geometry=df.geometry)
# plt = gdf[(gdf.gm_naam == option) & (gdf.recs == 'Wijk')].explore(column="a_inw",legend=True, legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"})
# plt.save('test.html')

if st.session_state["authentication_status"]:
    with st.expander('Home page', expanded=True):
        st.title("Jeugdzorg in kaart")
        st.write("Hier kan je kaarten bekijken")
        # capitalize the first character of username
        username = username.capitalize()
        if username in gdf.gm_naam.unique():
            # st.write(f"Je bent ingelogd als {username}")
            option = st.selectbox("Selecteer gebied:", np.append([username], gdf.gm_naam.unique()[1:]))
        else:
            # st.write(f"Je bent ingelogd als {username}")
            option = st.selectbox("Selecteer gebied:", np.append(["Nederland"], gdf.gm_naam.unique()[1:]))
        if option == "Nederland":
            st.image('./application/src/maps/Nederland.png')

            complete = False
        else:
            # try:
                # plt = gdf[(gdf.gm_naam == option) & (gdf.recs == 'Wijk')].explore(column="a_inw",legend=True, legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"})
                # plt.save('test.html')
                # output = st_folium(plt)
                # st.write(output)
                # TODO implementeerd ondeerstaande code (of selecteer wijk, zelfde manier als gemeente?)
                # wijk = st.selectbox("Selecteer wijk (optioneel):", np.append(["Gehele gemeente"], gdf[gdf.GM_NAAM == option].WK_NAAM.unique()))
                # gemeentecode = gdf[gdf.GM_NAAM == option].gemeentecode.unique()[0]
                # if wijk != "Gehele gemeente":
                #     wijkcode = gdf[gdf.WK_NAAM == wijk].WK_CODE.unique()[0]
                #     plt = gdf[gdf.WK_CODE == wijkcode].explore(column="perc_jhzv",tooltip=["WK_NAAM", "woonwaarde", "perc_jhzv"], popup=["WK_NAAM", "woonwaarde", "perc_jhzv"], legend="False", legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"}, vmin=4, vmax=15)
                #     output = st_folium(plt, returned_objects=[])
                #     st.write(output)

                # else:
                #     plt = gdf[gdf.gemeentecode == gemeentecode].explore(column="perc_jhzv", tooltip=["WK_NAAM", "woonwaarde", "perc_jhzv"], popup=["WK_NAAM", "woonwaarde", "perc_jhzv"], legend="False", legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"}, vmin=4, vmax=15)
                #     output = st_folium(plt, returned_objects=[])
                #     # this prevents a goofy error and the returning of single brackets with nothing inside because the st_folium library doesnt work well
                #     try:
                #          st.write(output[0])
                #     except:
                #          pass
                path_to_html = f"./application/src/maps/{option}.html" 

                # Read file and keep in variable
                with open(path_to_html,'r') as f: 
                    html_data = f.read()
                ## Show in webpage
                complete = True
        if complete:
            st.header("Show an external HTML")
            st.components.v1.html(html_data,height=600)
            # st.pyplot(fig)
elif authentication_status == False:
     st.error('Username/password is incorrect')