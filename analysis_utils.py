"""Conversão monetária, sem executar a navegação do Streamlit."""

import re
import numpy as np
import pandas as pd

def faixa_to_numeric(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    s_norm = s.replace('R$', '').replace('r$', '').replace('.', '').replace('\xa0','').replace(' ', '')
    s_norm = s_norm.replace(',', '.')
    # intervalo "100-200"
    m = re.search(r'(\d+(?:\.\d+)?)\s*[\-\–\—]\s*(\d+(?:\.\d+)?)', s_norm)
    if m:
        low = float(m.group(1)); high = float(m.group(2))
        return (low + high) / 2.0
    # "até N"
    m = re.search(r'(?i)até\.?\s*(\d+(?:[\.,]\d+)?)', s)
    if m:
        return float(m.group(1).replace('.', '').replace(',', '.'))
    # "acima de N" ou "mais de N"
    m = re.search(r'(?i)(acima|mais)\s*(de)?\s*(\d+(?:[\.,]\d+)?)', s)
    if m:
        return float(m.group(3).replace('.', '').replace(',', '.'))
    # "2000+"
    m = re.search(r'(\d+(?:\.\d+)?)\+', s_norm)
    if m:
        return float(m.group(1))
    # número simples
    m = re.search(r'(\d+(?:\.\d+)?)', s_norm)
    if m:
        return float(m.group(1))
    return np.nan
