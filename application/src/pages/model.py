# data imports
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# app imports
import uuid
import streamlit as st
import streamlit_authenticator as stauth
from utils import auth, get_data, logo, model

logo()

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    st.title("Model Page")
    st.write("Top 5 feature importances.")
    df = get_data()
    fig = model(df)
    st.pyplot(fig)
elif authentication_status == False:
     st.error('Username/password is incorrect')


if authentication_status:
    authenticator.logout('Logout', 'sidebar')

