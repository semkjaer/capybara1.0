import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import yaml

import streamlit_authenticator as stauth
import uuid

from utils import auth, logo

logo()

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

authenticator, config = auth()
name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
        if name == 'admin':
                with st.expander('Register user'):
                        if authenticator.register_user('Register user', preauthorization=False):
                                with open('./application/config.yaml', 'w') as file:
                                        yaml.dump(config, file)
                                        st.success('User registered successfully')
        st.title('Home page')
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





if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar')

