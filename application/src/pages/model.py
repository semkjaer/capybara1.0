import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def create_plot():
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)

    return fig


st.title("Model Page")
st.write("This is the model page.")

st.pyplot(create_plot())
