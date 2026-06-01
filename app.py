import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="Chuvas e Deslizamentos RJ", 
    page_icon="🌧️", 
    layout="wide"
)

BASE_DIR = Path(__file__).parent
CAMINHO_DADOS = BASE_DIR / "dados" / "simulacao_chuvas_deslizamentos_rj.csv"
CAMINHO_BANCO = BASE_DIR / "database" / "chuvas_rj.sqlite"

sns.set_theme(style="whitegrid")

# ---------------- CARREGAMENTO DE DADOS ----------------
@st.cache_data
def carregar_dados_csv():
    df = pd.read_csv(CAMINHO_DADOS)
    df["data"] = pd.to_datetime(df["data"])
    return df

def criar_banco_sqlite(df):
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)
    engine = create_engine(f"sqlite:///{CAMINHO_BANCO}")
    df.to_sql("chuvas", engine, if_exists="replace", index=False)
    return engine

df = carregar_dados_csv()
engine = criar_banco_sqlite(df)

st.title("Chuvas e Deslizamentos no Estado do Rio de Janeiro")

st.write("""
Este dashboard apresenta análises climáticas e de deslizamentos no Estado do Rio de Janeiro.
""")

# ---------------- SIDEBAR (FILTROS) ----------------
st.sidebar.header("Filtros")

anos = sorted(df["ano"].unique())
meses = sorted(df["mes"].unique())
municipios = sorted(df["municipio"].unique())
regioes = sorted(df["regiao_rj"].unique())
riscos = sorted(df["nivel_risco"].unique())

anos_sel = st.sidebar.multiselect("Ano", options=anos, default=anos)
meses_sel = st.sidebar.multiselect("Mês", options=meses, default=meses)
municipios_sel = st.sidebar.multiselect("Município", options=municipios, default=municipios)
regioes_sel = st.sidebar.multiselect("Região", options=regioes, default=regioes)
riscos_sel = st.sidebar.multiselect("Nível de Risco", options=riscos, default=riscos)

df_filtrado = df[
    (df["ano"].isin(anos_sel)) &
    (df["mes"].isin(meses_sel)) &
    (df["municipio"].isin(municipios_sel)) &
    (df["regiao_rj"].isin(regioes_sel)) &
    (df["nivel_risco"].isin(riscos_sel))
]

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ---------------- KPIs ----------------
st.subheader("Indicadores-chave de desempenho")

total_chuva = df_filtrado["chuva_mm"].sum()
media_chuva = df_filtrado["chuva_mm"].mean()
total_deslizamentos = df_filtrado["ocorrencias_deslizamento"].sum()
total_desalojados = df_filtrado["desalojados"].sum()

municipio_critico = (
    df_filtrado.groupby("municipio")["ocorrencias_deslizamento"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

correlacao = df_filtrado["chuva_mm"].corr(df_filtrado["ocorrencias_deslizamento"])

col1, col2, col3 = st.columns(3)
col1.metric("Volume Total de Chuva", f"{total_chuva:.2f} mm")
col2.metric("Média de Chuva", f"{media_chuva:.2f} mm")
col3.metric("Total de Deslizamentos", int(total_deslizamentos))

col4, col5, col6 = st.columns(3)
col4.metric("Total de Desalojados", int(total_desalojados))
col5.metric("Município Mais Crítico", municipio_critico)
col6.metric("Correlação Chuva x Desliz.", f"{correlacao:.2f}")

st.divider()

# ---------------- TABS ----------------
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Visão Geral", 
    "Análise Regional", 
    "Correlação e Sazonalidade", 
    "Consulta SQL", 
    "Dados"
])

with aba1:
    st.subheader("Evolução Temporal da Chuva")
    chuva_tempo = df_filtrado.groupby("data")["chuva_mm"].sum()
    fig1, ax1 = plt.subplots(figsize=(12,5))
    ax1.plot(chuva_tempo.index, chuva_tempo.values)
    ax1.set_xlabel("Data")
    ax1.set_ylabel("Chuva (mm)")
    st.pyplot(fig1)
    st.caption("""
    Este gráfico apresenta a evolução do volume de chuva ao longo do período analisado.
    Ele permite identificar os anos com maior intensidade de precipitação,
    auxiliando na detecção de períodos críticos que podem aumentar os riscos de
    alagamentos e deslizamentos.
    """)

    st.subheader("Evolução Temporal dos Deslizamentos")
    desliz_tempo = df_filtrado.groupby("data")["ocorrencias_deslizamento"].sum()
    fig2, ax2 = plt.subplots(figsize=(12,5))
    ax2.plot(desliz_tempo.index, desliz_tempo.values)
    ax2.set_xlabel("Data")
    ax2.set_ylabel("Deslizamentos")
    st.pyplot(fig2)
    st.caption("""
    Este gráfico mostra a variação das ocorrências de deslizamentos ao longo do tempo.
    A análise temporal permite verificar tendências de crescimento ou redução dos eventos
    e identificar períodos de maior vulnerabilidade ambiental.
    """)

with aba2:
    st.subheader("Ranking de Municípios Críticos")
    ranking = (
        df_filtrado.groupby("municipio")["ocorrencias_deslizamento"]
        .sum()
        .sort_values(ascending=False)
    )
    fig3, ax3 = plt.subplots(figsize=(12,5))
    ranking.plot(kind="bar", ax=ax3)
    ax3.set_ylabel("Ocorrências")
    st.pyplot(fig3)
    st.caption("""
    O ranking apresenta os municípios com maior número de ocorrências de deslizamentos.
    Essa visualização facilita a identificação das cidades mais vulneráveis e auxilia na
    priorização de ações preventivas e investimentos em infraestrutura.
    """)

with aba3:
    st.subheader("Correlação entre Chuva e Deslizamentos")
    fig4, ax4 = plt.subplots(figsize=(8,5))
    sns.scatterplot(
        data=df_filtrado,
        x="chuva_mm",
        y="ocorrencias_deslizamento",
        hue="nivel_risco",
        ax=ax4
    )
    st.pyplot(fig4)
    st.caption("""
    O gráfico de dispersão demonstra a relação entre o volume de chuva e a quantidade
    de deslizamentos registrados. Quanto mais próximos os pontos estiverem de uma tendência
    crescente, maior será a evidência de correlação entre as duas variáveis.
    """)

    st.subheader("Heatmap de Sazonalidade")
    heatmap_data = df_filtrado.pivot_table(
        values="ocorrencias_deslizamento",
        index="mes",
        columns="ano",
        aggfunc="sum"
    )
    fig5, ax5 = plt.subplots(figsize=(10,6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Reds", ax=ax5)
    st.pyplot(fig5)
    st.caption("""
    O heatmap permite identificar padrões sazonais de deslizamentos ao longo dos meses e anos.
    Tons mais intensos indicam maior quantidade de ocorrências, facilitando a identificação
    dos períodos mais críticos para o estado.
    """)

with aba4:
    st.subheader("Consulta SQL com SQLAlchemy")
    st.write("""
    Nesta seção, os dados originais foram gravados em um banco SQLite. A consulta abaixo 
    demonstra como usar SQL para extrair métricas de chuva e deslizamentos agrupadas por município.
    """)
    
    consulta = """
    SELECT 
        municipio, 
        SUM(chuva_mm) AS total_chuva_mm, 
        SUM(ocorrencias_deslizamento) AS total_deslizamentos,
        SUM(desalojados) AS total_desalojados
    FROM chuvas
    GROUP BY municipio
    ORDER BY total_deslizamentos DESC
    LIMIT 10
    """
    
    resultado_sql = pd.read_sql(consulta, engine)
    st.dataframe(resultado_sql, use_container_width=True)
    st.code(consulta, language="sql")

with aba5:
    st.subheader("Base Filtrada (Tabela Dinâmica)")
    st.dataframe(df_filtrado, use_container_width=True)
    st.caption("""
    A tabela dinâmica apresenta os dados detalhados após a aplicação dos filtros selecionados.
    Ela permite explorar informações específicas sobre municípios, regiões, chuvas,
    deslizamentos e níveis de risco.
    """)

# ---------------- CONCLUSÃO ----------------
st.divider()

col_conc1, col_conc2 = st.columns(2)

with col_conc1:
    st.subheader("Interpretação dos Resultados")
    st.write("""
    Os dados demonstram forte relação entre períodos de chuva intensa e aumento das ocorrências de deslizamentos.
    Os municípios da região serrana apresentaram maior vulnerabilidade em diversos períodos analisados.
    """)

with col_conc2:
    st.subheader("Conclusão Executiva")
    st.write("""
    O projeto permitiu identificar padrões climáticos e regiões críticas do Estado do Rio de Janeiro.
    As análises podem auxiliar estratégias preventivas e políticas públicas voltadas à redução de riscos ambientais.
    """)
