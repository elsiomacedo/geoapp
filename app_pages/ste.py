import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import openai
import io
import tempfile
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import plotly.express as px

# ======== CONFIGURAÇÕES ========
CAMINHO_CSV = './dados/DBTecno_All.csv'
HISTORICO_PATH = './historico_analises/'
os.makedirs(HISTORICO_PATH, exist_ok=True)

# ======== FUNÇÕES AUXILIARES ========
def tempo_para_minutos(tempo):
    horas, minutos = map(int, tempo.split(':'))
    return horas * 60 + minutos

def minutos_para_hhhmm(minutos):
    if pd.isna(minutos): return "000:00"
    h = int(minutos // 60)
    m = int(minutos % 60)
    return f"{h:03}:{m:02}"

def obter_modelos_anteriores():
    arquivos = [f for f in os.listdir(HISTORICO_PATH) if f.endswith(".txt")]
    textos = []
    for nome in arquivos:
        with open(os.path.join(HISTORICO_PATH, nome), 'r', encoding='utf-8') as f:
            textos.append(f.read())
    return "\n---\n".join(textos)

def gerar_analise_chatgpt(tabela_resumo, tabela_tecnicos):
    modelos_base = obter_modelos_anteriores()
    mes_atual = datetime.now().strftime("%B/%Y")
    prompt = f"""
    Mês de Referência: {mes_atual}
    Gere uma análise técnica detalhada da evolução da equipe de manutenção com base nos dados abaixo.
    Estruture o conteúdo com seções numeradas e inclua tabelas quando apropriado.

    {modelos_base}

    ---
    RESUMO MENSAL:
    {tabela_resumo.to_string(index=False)}

    RESUMO POR TÉCNICO:
    {tabela_tecnicos.to_string(index=False)}
    """
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um analista técnico especializado em equipes de manutenção."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return resposta.choices[0].message.content

def gerar_pdf_completo(analise):
    buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(buffer.name, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    estilo = ParagraphStyle('Justify', alignment=TA_LEFT, fontSize=11, leading=14)
    conteudo = [Paragraph("<b>Análise Técnica da Evolução da Equipe de Manutenção</b>", styles['Title']), Spacer(1, 12)]
    for linha in analise.split('\n'):
        conteudo.append(Paragraph(linha.strip(), estilo))
        conteudo.append(Spacer(1, 6))
    doc.build(conteudo)
    buffer.seek(0)
    return buffer.read()

def checar_modelos_existentes():
    arquivos = [f for f in os.listdir(HISTORICO_PATH) if f.endswith(".txt")]
    if not arquivos: return None, None
    mais_recente = max(arquivos, key=lambda x: os.path.getmtime(os.path.join(HISTORICO_PATH, x)))
    data_arquivo = datetime.fromtimestamp(os.path.getmtime(os.path.join(HISTORICO_PATH, mais_recente)))
    with open(os.path.join(HISTORICO_PATH, mais_recente), 'r', encoding='utf-8') as f:
        conteudo = f.read()
    return data_arquivo, conteudo

def salvar_novo_modelo(analise):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    nome = os.path.join(HISTORICO_PATH, f"analise_{timestamp}.txt")
    with open(nome, 'w', encoding='utf-8') as f:
        f.write(analise)


# ======== APLICAÇÃO PRINCIPAL STREAMLIT ========
df = pd.read_csv(CAMINHO_CSV)
df['Início'] = pd.to_datetime(df['Início'])
df['MesAno'] = df['Início'].dt.to_period('M').astype(str)
df['Tempo_min'] = df['Tempo'].apply(tempo_para_minutos)

st.title("Análise de Ordens de Serviço - Equipes de Manutenção")


# Filtros
tecnicos = ['Todos'] + sorted(df['TECNICO'].dropna().unique())
equipes = ['Todas'] + sorted(df['EQUIPE'].dropna().unique())
tipos = ['Todos'] + sorted(df['TIPO'].dropna().unique())
meses = ['Todos'] + sorted(df['MesAno'].unique())

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
# Agregações para Checklist
resumo_checklist = checklists.groupby('MesAno')['Tempo_min'].agg(
    Checklists='count',
    Tempo_Total_Checklist_min='sum',
    Tempo_Medio_Checklist_min='mean'
)
# Agregações para OS Corretiva
resumo_os = os_corretivas.groupby('MesAno')['Tempo_min'].agg(
    OS_Corretivas='count',
    Tempo_Total_OS_Corretiva_min='sum',
    Tempo_Medio_OS_Corretiva_min='mean'
)
# Mesclando os dois resumos
resumo_mensal = pd.concat([resumo_checklist, resumo_os], axis=1).fillna(0).reset_index()
# Convertendo os tempos para formato hhh:mm
resumo_mensal['Checklist TT'] = resumo_mensal['Tempo_Total_Checklist_min'].apply(minutos_para_hhhmm)
resumo_mensal['OS Corretiva TT'] = resumo_mensal['Tempo_Total_OS_Corretiva_min'].apply(minutos_para_hhhmm)
resumo_mensal['Checklist TM'] = resumo_mensal['Tempo_Medio_Checklist_min'].apply(minutos_para_hhhmm)
resumo_mensal['OS Corretiva TM'] = resumo_mensal['Tempo_Medio_OS_Corretiva_min'].apply(minutos_para_hhhmm)
resumo_mensal['OS Corretivas'] = resumo_mensal['OS_Corretivas']
    # Removendo colunas em minutos (valores não formatados)
resumo_mensal = resumo_mensal.drop(columns=[
    'Tempo_Total_Checklist_min',
    'Tempo_Medio_Checklist_min',
    'Tempo_Total_OS_Corretiva_min',
    'Tempo_Medio_OS_Corretiva_min',
    'OS_Corretivas'
    ])
resumo_mensal = resumo_mensal[[
    'MesAno', 'Checklists', 'Checklist TT', 'Checklist TM', 
    'OS Corretivas', 'OS Corretiva TT', 'OS Corretiva TM'
]]
# Resumo Técnico por Mês, Técnico e Equipe
resumo_tecnico = df_filtrado.groupby(['MesAno', 'TECNICO', 'EQUIPE']).agg(
    Total_Checklists=('TIPO', lambda x: (x == 'Checklist').sum()),
    Total_OS_Corretivas=('TIPO', lambda x: (x == 'OS Corretiva').sum()),
    Tempo_Total_min=('Tempo_min', 'sum'),
    Tempo_Medio_min=('Tempo_min', 'mean')
).reset_index()

# Converte tempo total e médio para hhh:mm
resumo_tecnico['Tempo_Total'] = resumo_tecnico['Tempo_Total_min'].apply(minutos_para_hhhmm)
resumo_tecnico['Tempo_Medio'] = resumo_tecnico['Tempo_Medio_min'].apply(minutos_para_hhhmm)
resumo_tecnico = resumo_tecnico[[
    'MesAno', 'TECNICO', 'EQUIPE', 'Total_Checklists', 'Total_OS_Corretivas',
    'Tempo_Total', 'Tempo_Medio'
]]


# 1.1 Dados Mensais
titulo = "1.1 Dados Mensais"
st.subheader(titulo)
exibir_aggrid(resumo_mensal, use_container_width=True, hide_index=True)

# 2.1 Evolução Mensal
titulo = "2.1 Evolução Mensal - Volume de Ordens por Mês"
st.subheader(titulo)
resumo_mensal['MesAnoFormatado'] = pd.to_datetime(resumo_mensal['MesAno']).dt.strftime('%m/%Y')
fig_plotly = px.line(resumo_mensal, x='MesAnoFormatado', y=['Checklists', 'OS Corretivas'], markers=True, title=titulo)
fig_plotly.update_traces(mode="lines+markers")
fig_plotly.update_layout(xaxis_title="Mês/Ano")
st.plotly_chart(fig_plotly, use_container_width=True)

# Agrupa por equipe e tipo, e conta quantos registros existem
if mes_sel != 'Todos': df_filtrado = df_filtrado[df_filtrado['MesAno'] == mes_sel]
df_agrupado = df_filtrado.groupby(['EQUIPE', 'TIPO']).size().reset_index(name='Quantidade')

# Filtra apenas Checklist e OS Corretiva (caso haja outros tipos)
df_agrupado = df_agrupado[df_agrupado['TIPO'].isin(['Checklist', 'OS Corretiva'])]

# Cria o gráfico de barras agrupadas
titulo = "3.1 Histórico por Equipe - Comparativo de Checklists e OS Corretivas"
st.subheader(titulo)

fig_barras = px.bar(
    df_agrupado,
    x='EQUIPE',
    y='Quantidade',
    color='TIPO',
    barmode='group',  # Pode trocar por 'stack' se quiser empilhado
    title=titulo,
    text='Quantidade'
)
fig_barras.update_layout(xaxis_title="Equipe", yaxis_title="Quantidade")
st.plotly_chart(fig_barras, use_container_width=True)


# 3.1 Resumo Técnico
titulo = "4.1 Resumo por Técnico"
st.subheader(titulo)
exibir_aggrid(resumo_tecnico)

# Derrete (melt) para formato longo
df_volume_tecnico = resumo_tecnico.melt(
    id_vars=['TECNICO'],
    value_vars=['Total_Checklists', 'Total_OS_Corretivas'],
    var_name='Tipo',
    value_name='Quantidade'
)

# Cria coluna com total de ordens
resumo_tecnico['Total_Ordens'] = (
    resumo_tecnico['Total_Checklists'] + resumo_tecnico['Total_OS_Corretivas']
)

# Ordena por total de ordens e pega os top 10
top_tecnicos = resumo_tecnico.sort_values(by='Total_Ordens', ascending=False).head(10)
print(top_tecnicos)
# Reformata para gráfico de barras com total de ordens por tipo
df_volume_top10 = top_tecnicos.melt(
    id_vars=['TECNICO'],
    value_vars=['Total_Checklists', 'Total_OS_Corretivas'],
    var_name='Tipo',
    value_name='Quantidade'
)

# Gráfico de barras horizontais - TOP 10 técnicos
st.subheader("4.1 Volume de Ordens - Top 10 Técnicos")
fig1 = px.bar(
    df_volume_top10,
    y='TECNICO',
    x='Quantidade',
    color='Tipo',
    barmode='stack',
    title="Top 10 Técnicos com Mais Ordens (Checklists + OS Corretivas)",
    orientation='h'
)
fig1.update_layout(yaxis_title="Técnico", xaxis_title="Quantidade Total de Ordens")
st.plotly_chart(fig1, use_container_width=True)

# Botão de geração
titulo = "Análise Técnica Gerada"
if st.button("Gerar Análise e Exportar Relatório PDF"):
    st.info("Análise em andamento. Aguarde alguns segundos...")
    with st.spinner("Gerando análise com ChatGPT..."):
        analise = gerar_analise_chatgpt(resumo_mensal, resumo_tecnico)
        st.markdown(f"### {titulo}")
        st.markdown(analise)

    data_ultima, analise_antiga = checar_modelos_existentes()
    dias = (datetime.now() - data_ultima).days if data_ultima else 999

    if data_ultima is None or dias > 30:
        salvar_modelo = st.checkbox("Deseja que essa nova análise sirva como modelo para futuros relatórios?")
        if salvar_modelo:
            salvar_novo_modelo(analise)

            st.success("Novo modelo salvo para aprendizado futuro.")

    relatorio_pdf = gerar_pdf_completo(analise)
    st.download_button("📄 Baixar Relatório Completo em PDF", relatorio_pdf, file_name="relatorio_completo.pdf", mime="application/pdf")