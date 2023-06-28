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

st.set_page_config(page_title='PinkCapybara', page_icon='favicon.ico', layout='wide', initial_sidebar_state='auto')
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
[data-baseweb="select"] {
    margin-top: -40px;
    margin-bottom: -20px;
}
.block-container {
    padding-top: 0px !important;
    padding-right: 20px !important;
    padding-left: 20px !important;
    margin-top: -70px !important;
}
.streamlit-expanderContent {
    margin-top: -40px !important;
}
[data-testid="stSidebarNav"] {  
    margin-bottom: 70px !important;
}
[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 225px !important;
    max-width: 225px !important;
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
        col1, _, _ = st.columns(3)
        if username in ts_total.gm_naam.unique():
            with col1:
                option = st.selectbox("Selecteer gebied:", np.append([username], ts_total.gm_naam.unique()[1:]))
        else:
            with col1:
                option = st.selectbox("Selecteer gebied:", np.append(['Amsterdam'], [x for x in ts_total.gm_naam.unique() if x != 'Amsterdam']))

        col1, col2 = st.columns(2)
        
        ts_plot = ts_total[ts_total.gm_naam == option]
        
        include_list = list(ts_plot.regio[:1])

        pio.renderers.default="notebook"
        # fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
        #                 if trace.name not in include_list else ())

        ts_plot1 = ts_plot.loc[ts_plot.year != '2023-01-01']
        ts_plot2 = ts_plot.loc[ts_plot.year.isin({'2022-01-01', '2023-01-01'})]
        # fig = px.line(ts_plot, x="year", y="p_jz_tn", color="regio")
        import plotly.graph_objects as go
        import matplotlib, random

        colors = [
                "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#800000", "#008000", "#000080", "#808000",
                "#800080", "#008080", "#FF8000", "#FF0080", "#80FF00", "#00FF80", "#0080FF", "#8000FF", "#804000", "#408000",
                "#004080", "#808040", "#800040", "#004080", "#408040", "#408080", "#804080", "#C00000", "#00C000", "#0000C0",
                "#C0C000", "#C000C0", "#00C0C0", "#FF4000", "#FF0040", "#40FF00", "#00FF40", "#0040FF", "#C04000", "#C00040",
                "#40C000", "#00C040", "#0040C0", "#C04040", "#40C040", "#40C0C0", "#C040C0", "#FF8000", "#FF0080", "#80FF00"
        ]

        data = []
        for wijk, color in zip(ts_plot.regio.unique(), colors[:len(ts_plot.regio.unique())]):
                ts_wijk1 = ts_plot1[(ts_plot1['regio'] == wijk)]
                trace1 = go.Scatter(x=ts_wijk1['year'],
                                    y=ts_wijk1['p_jz_tn'],
                                    name=wijk,
                                    legendgroup=wijk,
                                    line={'dash': 'solid', 'color': color},
                                    mode='lines')
                
                ts_wijk2 = ts_plot2[(ts_plot2['regio'] == wijk)]
                trace2 = go.Scatter(x=ts_wijk2['year'],
                                    y=ts_wijk2['p_jz_tn'],
                                    name=wijk,
                                    legendgroup=wijk,
                                    line={'dash': 'dash', 'color': color},
                                    showlegend=False)
                data.extend([trace1, trace2])

        fig = go.Figure(data=data)

        region_names = ts_plot['regio'].unique()
        default_active_regions = region_names[:6]
        fig.for_each_trace(lambda trace: trace.update(visible=True)
                        if trace.name in default_active_regions else trace.update(visible="legendonly"))

        fig.update_layout(
                shapes=[
                        dict(
                        type="rect",
                        xref="x",
                        yref="paper",
                        x0='2022',
                        y0=0,
                        x1='2023',
                        y1=1,
                        fillcolor="blue",
                        opacity=0.1,
                        layer="below",
                        line_width=0,
                        )
                ]
        )
        with col1:
                st.plotly_chart(fig, use_container_width=True)

        ts_bar_23_sorted = ts_plot.loc[(ts_plot['year'] == '2023-01-01')].sort_values(by = 'p_jz_tn', ascending=False)

        fig = px.bar(x=ts_bar_23_sorted['p_jz_tn'][:20].round(2), 
                y=ts_bar_23_sorted.regio[ts_bar_23_sorted['p_jz_tn'].index][:20],
                title='Wijken met het hoogst voorspelde percentage jongeren met jeugdzorg in 2023', 
                template='plotly_white')

        fig.update_layout(yaxis = {"categoryorder":"total ascending"},
                        xaxis_title="Percentage jongeren met jeugdzorg",
                        yaxis_title="Wijk")

        fig.update_traces(marker_color='#E2007A')
        with col2:
                st.plotly_chart(fig, use_container_width=True)

        ts_pie = ts_total[ts_total.gm_naam == option]
        ts_23_sorted = ts_pie.loc[(ts_pie['year'] == '2023-01-01')]
        ts_22_sorted = ts_pie.loc[(ts_pie['year'] == '2022-01-01')]
        
        fig = px.pie(names=ts_23_sorted.regio[ts_23_sorted['p_jz_tn'].index][:20].sort_values(ascending=True), 
                values=ts_23_sorted['p_jz_tn'][:20].round(2).sort_values(ascending=True), 
                title='Wijken en hun voorspelde percentage jongeren met jeugdzorg in 2023')
        fig.update_layout(colorway=shades_of_pink)
        with col1:
                st.plotly_chart(fig, use_container_width=True)

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
        with col2:
                st.plotly_chart(fig, use_container_width=True)

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
        with col1:
                st.plotly_chart(fig, use_container_width=True)
        with col2:
                st.image('importances.png')


elif authentication_status == False:
     st.error('Username/password is incorrect')