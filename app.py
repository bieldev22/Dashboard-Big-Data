import streamlit as st
from analysis_utils import faixa_to_numeric
from survey_data import is_demo

st.set_page_config(page_title="Dashboard Big Data", layout="wide")
if is_demo():
    st.caption("DEMONSTRAÇÃO · Dados fictícios; não representam a pesquisa original.")

pages = [
    st.Page("dados.py", title="Tabela de Dados", icon="📊"),
    st.Page("graf.py", title="Gráficos", icon="📈"),
    st.Page("models.py", title="Modelos", icon="🤖"),
]
st.navigation(pages).run()
