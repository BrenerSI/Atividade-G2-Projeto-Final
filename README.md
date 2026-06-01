# Dashboard Analítico de Chuvas e Deslizamentos no Estado do Rio de Janeiro

## 1. Descrição do projeto

Este projeto apresenta uma análise analítica e visual sobre eventos de chuvas intensas e deslizamentos de terra no Estado do Rio de Janeiro, com foco em vulnerabilidade climática, sazonalidade, regiões críticas e impactos sociais.

O projeto foi desenvolvido como referência para atividades de análise e visualização de dados utilizando Python.

A proposta busca demonstrar um fluxo completo de desenvolvimento de um projeto analítico:

1. entendimento do problema;
2. leitura e preparação dos dados;
3. criação de KPIs;
4. análise exploratória;
5. visualização de dados;
6. interpretação dos resultados;
7. construção de dashboard interativo com Streamlit;
8. publicação em repositório GitHub;
9. disponibilização do dashboard online.

---

## 2. Problema de negócio

Eventos climáticos extremos representam riscos significativos para municípios do Estado do Rio de Janeiro, especialmente em regiões urbanas com ocupação irregular e áreas de encosta.

O projeto busca responder às seguintes perguntas:

- Quais municípios apresentam maior volume de chuva?
- Quais cidades registram mais deslizamentos?
- Existem períodos sazonais mais críticos?
- Há correlação entre chuva intensa e aumento de deslizamentos?
- Quais regiões apresentam maior nível de risco?
- Quais municípios possuem maior número de desalojados?
- Existem padrões temporais relevantes ao longo dos anos?

---

## 3. Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Plotly
- GitHub

---

## 4. Estrutura do projeto

```text
Atividade-G2-Projeto-Final/
│
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/
│   └── simulacao_chuvas_deslizamentos_rj.csv
├── database/
│   └── simulacao_chuvas_deslizamentos_rj.sqlite
├── notebooks/
│   └── analise_chuvas_deslizamentos.ipynb
```

---

## 5. Como executar localmente

### 5.1 Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd Atividade_G2_Projeto_Final
```

### 5.2 Instalar dependências

```bash
pip install -r requirements.txt
```

### 5.3 Executar o dashboard

```bash
streamlit run app.py
```

---

## 6. KPIs utilizados

| KPI | Descrição |
|---|---|
| Chuva | Volume total e média mensal de precipitação |
| Deslizamentos | Total de ocorrências registradas |
| Desalojados | Análise de impactos sociais |
| Correlação | Relação entre chuva intensa e deslizamentos |

---

## 7. Funcionalidades do dashboard

O dashboard possui:

- filtros por município;
- filtros por região;
- filtros por ano;
- filtros por mês;
- filtros por nível de risco;
- KPIs dinâmicos;
- gráficos de evolução temporal das chuvas;
- gráficos de evolução temporal dos deslizamentos;
- gráficos de volume de chuva por município;
- gráficos de deslizamentos por município;
- gráficos comparativos por região;
- análise de correlação entre chuva e deslizamentos;
- consulta SQL demonstrativa;
- tabela interativa dos dados filtrados.

---

## 8. Principais insights esperados

O projeto permite identificar:

- municípios com maior volume de chuva;
- municípios com maior número de deslizamentos;
- regiões com maior vulnerabilidade ambiental;
- períodos do ano com maior incidência de chuvas intensas;
- períodos com maior concentração de deslizamentos;
- relação entre precipitação e ocorrência de deslizamentos;
- impactos sociais associados aos eventos climáticos;
- padrões sazonais de risco;
- áreas prioritárias para monitoramento e prevenção;
- tendências relevantes para o planejamento urbano e gestão de riscos.

---
