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

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

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
