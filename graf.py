import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns   
import pandas as pd
import numpy as np
from analysis_utils import faixa_to_numeric

st.markdown("# Gráficos 📈")
st.sidebar.markdown("# Gráficos 📈")
from survey_data import load_survey

df = load_survey()
df_jovens = df[df['Qual sua faixa etaria?'].astype(str).str.contains('18', na=False)]

pattern_18_24 = r'18\s*[-–—]\s*24|18\s*a\s*24|18\s*até\s*24|18-24|18–24|18 a 24'
mask_18_24 = df['Qual sua faixa etaria?'].astype(str).str.contains(pattern_18_24, case=False, regex=True, na=False)
if mask_18_24.sum() > 0:
    df_jovens = df[mask_18_24].copy()

lazer_counts = df_jovens['Local mais frequente de lazer:'].fillna('Não informado').value_counts()

plt.figure(figsize=(9,6))
explode = [0.07 if i==0 else 0 for i in range(len(lazer_counts))]
patches, texts, autotexts = plt.pie(lazer_counts, labels=None, autopct='%1.1f%%', startangle=140,
                                    explode=explode, pctdistance=0.75)
plt.title('Preferências de Lazer (18-24 anos)')
plt.legend(patches, lazer_counts.index, title='Local de Lazer', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.axis('equal')
plt.tight_layout()
st.pyplot(plt)
print("\n")
st.markdown("### Gráfico de Pizza: Preferências de Lazer entre Jovens (18-24 anos)")    

df['gasto_num'] = df['Gasto mensal não essencial (R$):'].apply(faixa_to_numeric)

gasto_por_idade = df.groupby('Qual sua faixa etaria?')['gasto_num'].agg(['median','count']).reset_index()

gasto_por_idade = gasto_por_idade.sort_values(by='median', na_position='last')

plt.figure(figsize=(11,6))
sns.barplot(data=gasto_por_idade, x='Qual sua faixa etaria?', y='median')
plt.xlabel('Faixa Etária')
plt.ylabel('Mediana do Gasto Não Essencial (R$)')
plt.title('Mediana do Gasto Não Essencial por Faixa Etária')
plt.xticks(rotation=45, ha='right')
for i, (_, row) in enumerate(gasto_por_idade.iterrows()):
    n = int(row['count'])
    y = row['median'] if not np.isnan(row['median']) else 0
    plt.text(i, y + max(1, 0.02 * (gasto_por_idade['median'].max() or 1)), f"n={n}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
st.pyplot(plt)
st.markdown("### Gráfico de Barras: Mediana do Gasto Não Essencial por Faixa Etária")   
print("\n")

cros = pd.crosstab(df['Qual sua faixa etaria?'], df['Seu canal de compra mais frequente:'])
cros['total'] = cros.sum(axis=1)
cros = cros.sort_values('total', ascending=False).drop(columns='total')

cros_lazer_idade = pd.crosstab(df['Local mais frequente de lazer:'].fillna('Não informado'),
                               df['Qual sua faixa etaria?'].fillna('Não informado'))
cros_lazer_idade = cros_lazer_idade.loc[cros_lazer_idade.sum(axis=1).sort_values(ascending=False).index]
plt.figure(figsize=(14,7))
ax = cros_lazer_idade.plot(kind='bar', width=0.8, figsize=(14,7), legend=False, edgecolor='black')

n_cols = cros_lazer_idade.shape[1]
palette = sns.color_palette('tab10', n_colors=n_cols)
for i, patch in enumerate(ax.patches):
    patch.set_facecolor(palette[i % n_cols])

ax.set_title('Canais de Lazer por Faixa Etária', fontsize=16, pad=12)
ax.set_ylabel('Número de pessoas', fontsize=12)

plt.xticks(rotation=40, ha='right')

ax.yaxis.grid(True, linestyle='--', linewidth=0.6, alpha=0.7)
ax.set_axisbelow(True)

handles = [plt.Rectangle((0,0),1,1, color=palette[i]) for i in range(n_cols)]
labels = cros_lazer_idade.columns.tolist()
plt.legend(handles, labels, title='Faixa etária', bbox_to_anchor=(0.5, -0.18), loc='upper center', ncol=min(n_cols, 6), frameon=False)

def fmt_val(v):
    if v >= 1000:
        return f"{v/1000:.1f}k"
    return str(int(v))
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(fmt_val(height),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=9, xytext=(0, 4), textcoords='offset points')

plt.tight_layout(rect=[0,0.05,1,1])
st.pyplot(plt)
st.markdown("### Gráfico de Barras: Canais de Lazer por Faixa   Etária")