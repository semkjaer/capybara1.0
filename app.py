import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = pd.ExcelFile('Wijkdata_Jeugdhulp_in_de_wijk.ods')

sheet_names = file.sheet_names
wijk = pd.read_excel(file, sheet_name=sheet_names[-3])  # wijk
gebr = pd.read_excel(file, sheet_name=sheet_names[-2])  # gebruik
det = pd.read_excel(file, sheet_name=sheet_names[-1])  # determinanten

file.close()

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

det

'yoyoyo'
