import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_data():
    file = pd.ExcelFile('Wijkdata_Jeugdhulp_in_de_wijk.ods')

    sheet_names = file.sheet_names
    det = pd.read_excel(file, sheet_name=sheet_names[-1])  # determinanten

    file.close()

    return det

data = load_data()
data

