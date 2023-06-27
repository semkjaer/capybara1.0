# data imports
import os
import pandas as pd
import geopandas as gpd
import numpy as np
# app imports
import uuid
import streamlit as st
import streamlit_authenticator as stauth
import plotly.io as pio
import plotly.express as px
from utils import auth, get_data, logo, model
import matplotlib.pyplot as plt

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
</style>
''', unsafe_allow_html=True)




authenticator, config = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')

if st.session_state["authentication_status"]:
    with st.expander('', expanded=True):
        st.title("Blik op de toekomst")
        ts_total = pd.read_csv("ts_total.csv")
        shades_of_pink = ['#FC6C85', '#FC8EAC', '#F88379', '#FF9999', '#FFD1DC', '#FFB6C1', '#FFB7C5', 
                    '#FFC1CC', '#F4C2C2', '#E75480', '#FF007F', '#A94064', '#FF6EC7', '#DE5D83', 
                    '#FF69B4', '#FFA6C9', '#FF8E8E', '#F4C2C2', '#FFBCD9', '#EFBBCC', '#F64A8A']
        if username in ts_total.gm_naam.unique():
            option = st.selectbox("Selecteer gebied:", np.append([username], ts_total.gm_naam.unique()[1:]))
        else:
            option = st.selectbox("Selecteer gebied:", ts_total.gm_naam.unique())
        ts_plot = ts_total[ts_total.gm_naam == option]
        
        # plot 1
        include_list = list(ts_plot.regio[:1])

        pio.renderers.default="notebook"
        fig = px.line(ts_plot, x="year", y="p_jz_tn", color="regio")
        fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                        if trace.name not in include_list else ())
        st.plotly_chart(fig)

        ts_bar_23_sorted = ts_plot.loc[(ts_plot['year'] == '2023-01-01')].sort_values(by = 'p_jz_tn', ascending=False)

        fig = px.bar(x=ts_bar_23_sorted['p_jz_tn'][:20].round(2), 
                y=ts_bar_23_sorted.regio[ts_bar_23_sorted['p_jz_tn'].index][:20],
                title='Wijken met het hoogst voorspelde percentage jongeren met jeugdzorg in 2023', 
                template='plotly_white')

        fig.update_layout(yaxis = {"categoryorder":"total ascending"},
                        xaxis_title="Percentage jongeren met jeugdzorg",
                        yaxis_title="Wijk")

        fig.update_traces(marker_color='#E2007A')
        st.plotly_chart(fig)

        ts_pie = ts_total[ts_total.gm_naam == option]
        ts_23_sorted = ts_pie.loc[(ts_pie['year'] == '2023-01-01')]
        ts_22_sorted = ts_pie.loc[(ts_pie['year'] == '2022-01-01')]
        
        fig = px.pie(names=ts_23_sorted.regio[ts_23_sorted['p_jz_tn'].index][:20].sort_values(ascending=True), 
                values=ts_23_sorted['p_jz_tn'][:20].round(2).sort_values(ascending=True), 
                title='Wijken en hun voorspelde percentage jongeren met jeugdzorg in 2023')
        fig.update_layout(colorway=shades_of_pink)
        st.plotly_chart(fig)

        fig = px.bar(x=ts_22_sorted.regio[ts_22_sorted['a_soz_ao'].index][:20].sort_values(ascending=True), 
                y=ts_22_sorted['a_soz_ao'][:20].round(2).sort_values(ascending=True), 
                title='Aantal WAO-gerechtigden in 2022', 
                template='plotly_white')

        fig.add_bar(x=['Gemiddelde in Nederland'], 
                    y=[ts_total.loc[(ts_total['year'] == '2022-01-01')]['a_soz_ao'].mean()], 
                    name='Nederlands gemiddelde', 
                    showlegend=False)

        fig.update_layout(xaxis_title="Wijken",
                        yaxis_title="Aantal WAO-gerechtigden")
        fig.update_traces(marker_color='#E2007A')
        st.plotly_chart(fig)

        fig = px.bar(x=ts_22_sorted.regio[ts_22_sorted['bev_dich'].index][:20].sort_values(ascending=True), 
                y=ts_22_sorted['bev_dich'][:20].round(2).sort_values(ascending=True), 
                title='Bevolkingsdichtheid in 2022', 
                template='plotly_white')

        fig.add_bar(x=['Gemiddelde in Nederland'], 
                    y=[ts_total.loc[(ts_total['year'] == '2022-01-01')]['bev_dich'].mean()], 
                    name='Nederlands gemiddelde', 
                    showlegend=False)

        fig.update_layout(xaxis_title="Wijken",
                        yaxis_title="Bevolkingsdichtheid")
        fig.update_traces(marker_color='#E2007A')
        st.plotly_chart(fig)

        st.image('importances.png')


elif authentication_status == False:
     st.error('Username/password is incorrect')