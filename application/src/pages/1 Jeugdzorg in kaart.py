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

df = get_data()
gdf = gpd.GeoDataFrame(df, crs="EPSG:28992", geometry=df.geometry)
fig, ax = plt.subplots(figsize = (12,12))
ax.set_axis_off()

if st.session_state["authentication_status"]:
    with st.expander('Home page', expanded=True):
        st.title("Jeugdzorg in kaart")
        st.write("This is the model page.")
        with open("gemeentes.txt") as file:
            for line in file:
                options = line.split(",")
        option = st.selectbox("Selecteer gebied:", np.append(["Nederland"], gdf.GM_NAAM.unique()[1:]))
        if option == "Nederland":
            gdf.plot(ax=ax, column="AANT_INW",legend=True, legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"})
            complete = True
        else:
            try:
                gemeentecode = gdf[gdf.GM_NAAM == option].gemeentecode.unique()[1]
                gdf[gdf.gemeentecode == gemeentecode].plot(ax=ax, column="AANT_INW",legend=True, legend_kwds={"label": "Aantal mensen per gemeente", "orientation": "horizontal"}, edgecolor="black")
                complete = True
            except:
                st.write("Helaas is er voor deze gemeente geen data beschikbaar")
                complete = False
        if complete:
            st.pyplot(fig)
elif authentication_status == False:
     st.error('Username/password is incorrect')

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

