import streamlit as st
import sklearn as sk
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
import matplotlib.pyplot as plt
import seaborn as sns   
import pandas as pd
from analysis_utils import faixa_to_numeric
from sklearn.decomposition import PCA

CARD_CSS ="""
<style>
.persona-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  padding: 14px;
  margin: 8px 6px;
  font-family: "Inter", sans-serif;
  color: #202124;
}
.persona-id { font-size:16px; font-weight:700; margin-bottom:6px; }
.persona-count { color:#666; font-size:12px; margin-bottom:8px; }
.persona-canal { color:#666; font-size:12px; margin-bottom:8px; }
.persona-lazer { color:#666; font-size:12px; margin-bottom:8px; }
.persona-idade { color:#666; font-size:12px; margin-bottom:8px; }
.persona-plataforma { color:#666; font-size:12px; margin-bottom:8px; }
.persona-metrics { display:flex; gap:10px; margin-bottom:8px; }
.persona-median_gasto { background:#0D0D0D; color:#ffffff; padding:6px 8px; border-radius:8px; font-size:13px; }
.small-note { font-size:12px; color:#777; }
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

st.markdown("# Modelos 🤖")
st.sidebar.markdown("# Modelos 🤖")

from survey_data import load_survey

df = load_survey()

categorical_cols = ['Você é um profissional:','Qual sua faixa etaria?','Gênero:', 'Município onde reside:',
                    'Faixa de renda mensal:','Seu canal de compra mais frequente:', 'Categoria do seu consumo mensal principal:',
                    'Gasto mensal não essencial (R$):', 'Local mais frequente de lazer:', 'Frequências de lazer semanal:',
                    'Estilo de vida predominante:', 'Plataforma onde acompanha marcas:', 'Frequência de compras online:']


df_encoded = pd.get_dummies(df[categorical_cols])
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_encoded)

for k in [2,3,4,5,6]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(df_scaled)
    labels = km.labels_
    print(k, 'silhouette=', silhouette_score(df_scaled, labels),
              'CH=', calinski_harabasz_score(df_scaled, labels))

k_final = 4
km = KMeans(n_clusters=k_final, random_state=42, n_init=50)
df['Cluster'] = km.fit_predict(df_scaled)

df['gasto_num'] = df['Gasto mensal não essencial (R$):'].apply(faixa_to_numeric)
st.columns(1)[0].markdown("### Estatísticas dos Clusters")
for cluster_id, group in df.groupby('Cluster')[categorical_cols].agg(lambda s: s.mode()[0]).iterrows():
    idade= group['Qual sua faixa etaria?']
    lazer= group['Local mais frequente de lazer:']
    canal= group['Seu canal de compra mais frequente:']
    plataforma= group['Plataforma onde acompanha marcas:']
    cluster_frame = df.loc[df['Cluster'] == cluster_id]
    median_gasto = cluster_frame['gasto_num'].median()
    count = len(cluster_frame)
    card_html = f"""
    <div class="persona-card">
      <div class="persona-id">Cluster {cluster_id}</div>
      <div class="persona-count">Número de membros: {count}</div>
      <div class="persona-idade">Faixa etária: {idade}</div>
      <div class="persona-lazer">Lazer: {lazer}</div>
      <div class="persona-canal">Canal de compra: {canal}</div>
      <div class="persona-plataforma">Plataforma: {plataforma}</div>
      <div class="persona-metrics">
        <div class="persona-median_gasto">Mediana Gasto Não Essencial: R$ {median_gasto:.2f}</div>
      </div>
    </div>
    """
    st.columns(1)[0].markdown(card_html, unsafe_allow_html=True)

pca = PCA(n_components=2)
proj = pca.fit_transform(df_scaled)
plt.scatter(proj[:,0], proj[:,1], c=df['Cluster'])
plt.title('PCA 2D dos clusters')
st.pyplot(plt)
st.markdown("### Visualização PCA dos Clusters")
