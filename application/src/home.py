import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_authenticator as stauth
import uuid

from utils.auth import auth
from utils.logo import logo

logo()

if 'key' not in st.session_state:
            st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
        st.title('Home page')
        st.write('welcome', name)
elif authentication_status == False:
        st.error('Username/password is incorrect')





if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar')
