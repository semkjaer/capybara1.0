import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import uuid

from utils import auth, logo

logo()

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_data
def load_data():
    file = pd.ExcelFile('Wijkdata_Jeugdhulp_in_de_wijk.ods')

    sheet_names = file.sheet_names
    det = pd.read_excel(file, sheet_name=sheet_names[-1])  # determinanten

    file.close()

    for col in det.columns:
        det[col] = det[col].apply(lambda x: x if x != '.' else np.nan)

    return det

if authentication_status:
     st.title('Data page')
     data = load_data()
     data
elif authentication_status == False:
     st.error('Username/password is incorrect')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')


