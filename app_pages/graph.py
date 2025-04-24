import pandas as pd
import streamlit as st
import os
import plotly.express as px
from utils.tools import carregar_dados_csv, carregar_dados_excel, tempo_para_minutos, minutos_para_hhhmm
from utils.graph_tools import grafico_tempo_medio
from datetime import datetime

# ======== CONFIGURAÇÕES ========
CAMINHO_CSV = './dados/DBTecno_All.csv'
HISTORICO_PATH = './historico_analises/'
os.makedirs(HISTORICO_PATH, exist_ok=True)

# ======== FUNÇÕES AUXILIARES ========

# ======== APLICAÇÃO PRINCIPAL STREAMLIT ========
df = carregar_dados_csv(CAMINHO_CSV)
df['Início'] = pd.to_datetime(df['Início'])
df['MesAno'] = df['Início'].dt.to_period('M').astype(str)
df['Tempo_min'] = df['Tempo'].apply(tempo_para_minutos)

# Filtros
tecnicos = ['Todos'] + sorted(df['TECNICO'].dropna().unique())
equipes = ['Todas'] + sorted(df['EQUIPE'].dropna().unique())
tipos = ['Todos'] + sorted(df['TIPO'].dropna().unique())
meses = ['Todos'] + sorted(df['MesAno'].unique(), reverse=True)

st.sidebar.subheader("Filtros")
tecnico_sel = st.sidebar.selectbox("Técnico:", tecnicos)
equipe_sel = st.sidebar.selectbox("Equipe:", equipes)
tipo_sel = st.sidebar.selectbox("Tipo:", tipos)
mes_sel = st.sidebar.selectbox("Mês/Ano:", meses)

# Aplicar filtros
df_filtrado = df.copy()
if tecnico_sel != 'Todos': df_filtrado = df_filtrado[df_filtrado['TECNICO'] == tecnico_sel]
if equipe_sel != 'Todas': df_filtrado = df_filtrado[df_filtrado['EQUIPE'] == equipe_sel]
if tipo_sel != 'Todos': df_filtrado = df_filtrado[df_filtrado['TIPO'] == tipo_sel]

# Resumo Mensal
checklists = df_filtrado[df_filtrado['TIPO'] == 'Checklist']
os_corretivas = df_filtrado[df_filtrado['TIPO'] == 'OS Corretiva']

resumo_checklist = checklists.groupby('MesAno')['Tempo_min'].agg(
    Checklists='count',
    Tempo_Total_Checklist_min='sum',
    Tempo_Medio_Checklist_min='mean'
)

resumo_os = os_corretivas.groupby('MesAno')['Tempo_min'].agg(
    OS_Corretivas='count',
    Tempo_Total_OS_Corretiva_min='sum',
    Tempo_Medio_OS_Corretiva_min='mean'
)

resumo_mensal = pd.concat([resumo_checklist, resumo_os], axis=1).fillna(0).reset_index()
resumo_mensal['MesAnoFormatado'] = pd.to_datetime(resumo_mensal['MesAno']).dt.strftime('%m/%Y')

# Gráfico 1: Evolução Mensal
fig_plotly = px.line(resumo_mensal, x='MesAnoFormatado', y=['Checklists', 'OS_Corretivas'], markers=True,
                     title="Evolução Mensal - Volume de Ordens por Mês")
fig_plotly.update_traces(mode="lines+markers")
fig_plotly.update_layout(xaxis_title="Mês/Ano")
st.plotly_chart(fig_plotly, use_container_width=True)

# Gráfico 2: Comparativo por Equipe
df_filtrado['MesAno'] = df_filtrado['MesAno'].astype(str)  # Garantir que MesAno seja string no formato yyyy-mm
if mes_sel != 'Todos': df_filtrado = df_filtrado[df_filtrado['MesAno'] == mes_sel]
df_agrupado = df_filtrado.groupby(['EQUIPE', 'TIPO']).size().reset_index(name='Quantidade')
df_agrupado = df_agrupado[df_agrupado['TIPO'].isin(['Checklist', 'OS Corretiva'])]

fig_barras = px.bar(df_agrupado, x='EQUIPE', y='Quantidade', color='TIPO', barmode='group', text='Quantidade',
                    title="Histórico por Equipe - Comparativo de Checklists e OS Corretivas")
fig_barras.update_layout(xaxis_title="Equipe", yaxis_title="Quantidade")
st.plotly_chart(fig_barras, use_container_width=True)

# Gráfico 3: Top 10 Técnicos
resumo_tecnico = df_filtrado.groupby(['MesAno', 'TECNICO', 'EQUIPE']).agg(
    Total_Checklists=('TIPO', lambda x: (x == 'Checklist').sum()),
    Total_OS_Corretivas=('TIPO', lambda x: (x == 'OS Corretiva').sum()),
    Tempo_Total_min=('Tempo_min', 'sum'),
    Tempo_Medio_min=('Tempo_min', 'mean')
).reset_index()

resumo_tecnico['Total_Ordens'] = resumo_tecnico['Total_Checklists'] + resumo_tecnico['Total_OS_Corretivas']
top_tecnicos = resumo_tecnico.groupby('TECNICO', as_index=False).agg(
    Total_Checklists=('Total_Checklists', 'sum'),
    Total_OS_Corretivas=('Total_OS_Corretivas', 'sum'),
    Total_Ordens=('Total_Ordens', 'sum')
).sort_values(by='Total_Ordens', ascending=False).head(10)  # Limitar aos 10 mais

fig_top_tecnicos = px.bar(
    top_tecnicos.sort_values(by='Total_Ordens', ascending=True),  # Ordenar do menor para o maior
    y='TECNICO',
    x=['Total_Checklists', 'Total_OS_Corretivas'],
    orientation='h',
    title="Volume de Ordens - Top 10 Técnicos (Empilhado por Tipo)",
    labels={'value': 'Quantidade', 'variable': 'Tipo'}
)
fig_top_tecnicos.update_layout(
    barmode='stack',
    yaxis_title="Técnico",
    xaxis_title="Quantidade Total de Ordens"
)
st.plotly_chart(fig_top_tecnicos, use_container_width=True)


