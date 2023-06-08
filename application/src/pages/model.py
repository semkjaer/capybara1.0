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
from utils.auth import auth
from utils.logo import logo

logo()

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_data
def get_data():
    file = pd.ExcelFile('Wijkdata_Jeugdhulp_in_de_wijk.ods')

    sheet_names = file.sheet_names

    wijk = pd.read_excel(file, sheet_name=sheet_names[-3])  # wijk
    gebr = pd.read_excel(file, sheet_name=sheet_names[-2])  # gebruik
    det = pd.read_excel(file, sheet_name=sheet_names[-1])  # determinanten

    file.close()

    df = det.copy()
    # als je wijk en gemeentecode hebt heb je wijkcode en gemeentenaam niet nodig
    df = df.merge(wijk[['wijk', 'gemeentecode']], on='wijk', how='left')
    # per_jhzv : aandeel jeugdigen met jeugdhulp zonder verblijf, waargenomen -> target variable
    df = df.merge(gebr[['wijk', 'perc_jhzv']], on='wijk', how='left')

    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if x != '.' else np.nan)

    # TODO is nu missig values vullen met gemiddelde hoe willen we dat doen?
    df.fillna(df.mean(), inplace=True)

    # hun schatting root mean squared error (residu = schatting - waargenomen)
    for col in gebr.columns:
        gebr[col] = gebr[col].apply(lambda x: x if x != '.' else np.nan)

    # drop missende schattingen en bereken RMSE
    # original_rmse = str((gebr.dropna(subset='residu')['residu']**2).mean()**0.5)

    # buurt_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/buurt_2022_v1.shp')
    wijk_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/wijk_2022_v1.shp')
    # gemeente_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/gemeente_2022_v1.shp')

    wijk_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/wijk_2022_v1.shp')
    wijk_geo['WK_CODE'] = wijk_geo['WK_CODE'].apply(lambda x: x[2:]).astype('float')
    wijk_geo['GM_CODE'] = wijk_geo['GM_CODE'].apply(lambda x: x[2:]).astype('float')
    wijk_final = df.merge(wijk_geo, left_on=['wijk', 'gemeentecode'], right_on=['WK_CODE', 'GM_CODE'], how='left')
    for col in wijk_final.columns:
        wijk_final[col] = wijk_final[col].apply(lambda x: x if x != int(-99999999) else np.nan)

    df = wijk_final.fillna(wijk_final.mean())
    return fig

if st.session_state["authentication_status"]:
    st.title("Model Page")
    st.write("This is the model page.")
    st.pyplot(get_data())
elif authentication_status == False:
     st.error('Username/password is incorrect')


if authentication_status:
    authenticator.logout('Logout', 'sidebar')


