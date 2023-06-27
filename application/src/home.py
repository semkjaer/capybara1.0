import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yaml
from yaml.loader import SafeLoader

import streamlit_authenticator as stauth
import uuid

from utils import auth, logo, registration_email

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

# st.markdown(
# """
# <style>
# .stApp {
# background-image: url('application/src/background_login.jpg');
# background-attachment: fixed;
# background-size: cover
# }
# </style>
# """, unsafe_allow_html=True)

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
[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 225px !important;
    max-width: 225px !important;
}
</style>
''', unsafe_allow_html=True)
authenticator, config = auth()


if 'login' not in st.session_state:
        st.session_state['admin'] = False


with st.expander('Login', expanded=True):
        name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
        if name == 'admin':
                with st.expander('Preauthorize user'):
                        st.session_state['register'] = False
                        form = st.form(key='preauthorize')
                        email = form.text_input(label='email')
                        submit_button = form.form_submit_button(label='Submit')
                        if submit_button:
                                with open('./application/config.yaml', 'a') as file:
                                        print('email')
                                        file.write(f'  - {email}\n')
                                        registration_email(email, registered=False)
                                st.success('email preauthorized!')
        with st.expander('Home page', expanded=True):
                st.markdown('''
                Welkom op **capybara1.0** hét dashboard dat inzicht biedt in de jeugdzorg!

                De pagina 'Jeugdzorg in Kaart' bevat kaarten en grafieken om de jeugdzorg in
                Nederland inzichtelijk te maken. Aan de hand van data van het CBS kun u hier
                de bezettingsgraad en risicofactoren van verschillende gemeentes en wijken
                met elkaar vergelijken.

                Op de pagina 'Blik op de toekomst' bevat de resultaten van vindt u de 
                resultaten van verschillende analyses die inzicht dienen te bieden in de
                toekomst van de jeugdzorg en de factoren die hier aan bij kunnen dragen.
                ''')
elif authentication_status == False:
        st.error('Username/password is incorrect')

if not st.session_state["authentication_status"]:
        with st.expander('Register'):
                old_users = [x for x in config['credentials']['usernames']]
                try:
                        if authenticator.register_user('Register user', preauthorization=True):
                                with open('./application/config.yaml', 'w') as file:
                                        yaml.dump(config, file)
                                        st.success('User registered successfully')
                                        for user in config['credentials']['usernames']:
                                                if (user in old_users) == False:
                                                        registration_email(config['credentials']['usernames'][user]['email'], registered=False)
                except Exception as e:
                        st.error(str(e))

if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar')

