import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import uuid
import os

def auth():
        print(os.getcwd())
        with open('config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)

                authenticator = stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
                )

        return authenticator