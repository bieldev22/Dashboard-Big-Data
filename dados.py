import streamlit as st  
import pandas as pd


st.markdown("# Tabela de Dados 📊")
st.sidebar.markdown("# Tabela de Dados 📊")
from survey_data import load_survey

df = load_survey()
st.dataframe(df)