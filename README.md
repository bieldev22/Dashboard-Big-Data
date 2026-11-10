# Dashboard Big Data — análise de consumo e lazer

Projeto de Gabriel Alves de Alencar com preparação de respostas de pesquisa,
visualização de dados e segmentação por K-Means. Este repositório reúne o
dashboard Streamlit existente e o script de análise `BIG_DATA.py`.

## O que o código faz

- Converte faixas de gasto em valores numéricos aproximados.
- Compara preferências de lazer e mediana de gastos por faixa etária.
- Codifica variáveis categóricas com `pandas.get_dummies` e usa `StandardScaler`.
- Compara agrupamentos com inércia, Silhouette e Calinski-Harabasz.
- Executa K-Means com quatro grupos e apresenta a projeção PCA em duas dimensões.

Os resultados descrevem os dados carregados. Não demonstram causalidade, não
validam representatividade da pesquisa e não constituem previsão de consumo.
Faixas monetárias são aproximações e quatro grupos são uma escolha exploratória.

## Executar a análise

Requisitos: Python 3.11 ou superior. Não é necessário Streamlit para este comando.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-analysis.txt
.\.venv\Scripts\python BIG_DATA.py
```

No Linux/macOS, use `.venv/bin/python`. O script abre gráficos com Matplotlib
e imprime métricas e resumos no terminal. Em ambiente sem janela, use o backend
`Agg` (`$env:MPLBACKEND='Agg'` no PowerShell); nesse caso não há janelas gráficas.

## Dashboard existente

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O dashboard usa navegação entre tabela, gráficos e modelos. Sua publicação foi
informada em <https://dashboard-big-data.streamlit.app/>. A disponibilidade
depende do Streamlit Community Cloud, que pode suspender o app por inatividade.
Publicar o código no GitHub não altera essa política. Não há deployment de
backend Streamlit na Vercel neste repositório.

## Dados e privacidade

Sem configuração, a fonte compartilhada gera **80 registros inteiramente
fictícios**, com semente fixa, para demonstrar o processamento sem divulgar
respostas da pesquisa. Esses números não são resultados reais do estudo.

Para trabalhar com uma fonte autorizada, defina `SURVEY_CSV_PATH` (arquivo local)
ou `SURVEY_CSV_URL` (CSV acessível ao processo) no ambiente. `.env.example`
documenta os nomes; os programas não carregam `.env` automaticamente. São lidas
somente as 13 colunas categóricas declaradas em `survey_data.py`. A seleção de
colunas reduz exposição, mas não garante anonimização de dados reais. Use apenas
fontes cuja divulgação seja autorizada e mantenha dados privados fora do Git.

A URL da planilha original foi retirada da versão atual. Ela pode continuar no
histórico anterior do repositório; o histórico foi preservado, sem force push.
Não foram incluídos CSVs reais, credenciais ou respostas individuais nesta atualização.

## Estrutura e limites

| Arquivo | Responsabilidade |
| --- | --- |
| `BIG_DATA.py` | Análise exploratória completa executada no terminal |
| `survey_data.py` | Fonte de demonstração ou leitura de CSV autorizado |
| `analysis_utils.py` | Conversão de faixas monetárias compartilhada pelo dashboard |
| `app.py` | Entrada e navegação do Streamlit |
| `dados.py` | Tabela dos dados usados |
| `graf.py` | Gráficos exploratórios |
| `models.py` | Segmentação e visualização dos grupos |

O script foi escrito para bases com ao menos 11 registros e diversidade
suficiente para comparar até dez grupos. CSVs vazios, com colunas ausentes,
com poucos registros ou sem diversidade exigem tratamento antes da análise.
Não há banco persistente, autenticação ou integração ManyChat neste projeto.
Não são versionados ambientes virtuais, caches, arquivos privados ou segredos.

## Verificação

Com as dependências do dashboard instaladas, execute `python -m unittest -v`.
Os testes verificam conversão monetária, dados fictícios reproduzíveis, exclusão
de colunas identificáveis e execução das três páginas com estatísticas por grupo.
