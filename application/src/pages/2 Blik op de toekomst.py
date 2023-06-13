# data imports
import os
import pandas as pd
import geopandas as gpd
# app imports
import uuid
import streamlit as st
import streamlit_authenticator as stauth
from utils import auth, get_data, logo, model

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
.st-dq { background-color: #FFFFFF; }
.streamlit-expander { background-color: #FFFFFF; }
.css-dbxtwr { display: none; }
</style>
''', unsafe_allow_html=True)
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
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')

if st.session_state["authentication_status"]:
    st.title("Blik op de toekomst")
    st.write("Top 5 feature importances.")
    df = get_data()
    fig = model(df)
    st.pyplot(fig)
elif authentication_status == False:
     st.error('Username/password is incorrect')
