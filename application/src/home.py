import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import uuid


st.set_page_config(
        page_title="Home",
)

if 'key' not in st.session_state:
        st.session_state['key'] = uuid.uuid1()

with open('./application/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
     st.write('Welcome *%s*' % (name))
     st.title('Some content')
elif authentication_status == False:
     st.error('Username/password is incorrect')
elif authentication_status == None:
     st.warning('Please enter your username and password')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')


st.title("Home Page")
st.write("This is the home page.")