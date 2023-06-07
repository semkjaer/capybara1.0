import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_authenticator as stauth
import uuid

from utils.auth import auth

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_data
def create_plot():
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)

    return fig

if st.session_state["authentication_status"]:
    st.title("Model Page")
    st.write("This is the model page.")
    st.pyplot(create_plot())
elif authentication_status == False:
     st.error('Username/password is incorrect')


if authentication_status:
    authenticator.logout('Logout', 'sidebar')


