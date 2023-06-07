import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import uuid

def auth():
        with open('./application/config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)

                authenticator = stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
                )

        return authenticator