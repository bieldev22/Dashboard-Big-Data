import streamlit as st  
import pandas as pd


st.markdown("# Tabela de Dados 📊")
st.sidebar.markdown("# Tabela de Dados 📊")
url= "https://docs.google.com/spreadsheets/d/1Y5fFvU-r9ZrPJ3xAq_ANn4LK3qd8azr4mpcTqPgaCYw/export?format=csv"
df= pd.read_csv(url)
st.dataframe(df)