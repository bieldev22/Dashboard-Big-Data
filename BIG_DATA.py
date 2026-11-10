import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
import seaborn as sns
import re

from survey_data import is_demo, load_survey

# A pesquisa original não é distribuída. Dados fictícios por padrão.
df = load_survey()
if is_demo():
    print('DEMONSTRAÇÃO: dados sintéticos; não representam a pesquisa original.')

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

try:
    df_jovens
except NameError:
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
plt.show()
print("\n")

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
plt.show()
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
plt.show()

categorical_cols = ['Você é um profissional:','Qual sua faixa etaria?','Gênero:', 'Município onde reside:',
                    'Faixa de renda mensal:','Seu canal de compra mais frequente:', 'Categoria do seu consumo mensal principal:',
                    'Gasto mensal não essencial (R$):', 'Local mais frequente de lazer:', 'Frequências de lazer semanal:',
                    'Estilo de vida predominante:', 'Plataforma onde acompanha marcas:', 'Frequência de compras online:']

df_encoded = pd.get_dummies(df[categorical_cols])
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_encoded)

inertia = []
K_range = range(2,11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(df_scaled)
    inertia.append(km.inertia_)

plt.plot(K_range, inertia, marker='o')
plt.xlabel('k'); plt.ylabel('Inertia'); plt.show()

for k in [2,3,4,5,6]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(df_scaled)
    labels = km.labels_
    print(k, 'silhouette=', silhouette_score(df_scaled, labels),
              'CH=', calinski_harabasz_score(df_scaled, labels))

k_final = 4
km = KMeans(n_clusters=k_final, random_state=42, n_init=50)
df['Cluster'] = km.fit_predict(df_scaled)

print(df.groupby('Cluster')['gasto_num'].median())
print(df.groupby('Cluster')[categorical_cols].agg(lambda s: s.mode()[0])) # calculate mode for original categorical columns

pca = PCA(n_components=2)
proj = pca.fit_transform(df_scaled)
plt.scatter(proj[:,0], proj[:,1], c=df['Cluster'])
plt.title('PCA 2D dos clusters'); plt.show()
