from utils.tools import gerar_referencia, filtrar_por_referencia, carregar_dados_csv, carregar_dados_excel
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from components import titulo_page
from metricas import metricascorretivas, hist_natureza, hist_tipo

# Constantes de estilo
def get_border_config():
    return {
        "color": "#003f5c",
        "radius": "10px",
        "width": "2px"
    }

# Utilitários de carregamento de dados
@st.cache_data
def carregar_dados():
    return carregar_dados_csv("dados/DBCorretivas.csv",
                            parse_dates=["Data/Hora Abertura", "Data/Hora Início", "Data/Hora Término"])

# Gráficos

def criar_grafico_linhas(df, categorias, titulo):
    fig = go.Figure()
    for categoria in categorias:
        fig.add_trace(go.Scatter(
            x=df['Referência'],
            y=df[categoria],
            mode='lines+markers+text',
            name=categoria,
            text=df[categoria],
            textposition='top center'
        ))
    fig.update_layout(
        title=titulo,
        xaxis_title='Referência (Ano-Mês)',
        yaxis_title='Quantidade',
        xaxis_tickangle=-45,
        hovermode='x unified',
        legend_title_text='Categorias',
        legend=dict(orientation="h", yanchor="top", y=-0.4, xanchor="center", x=0.5),
        margin=dict(b=120),
        template='plotly_white'
    )
    return fig

def exibir_com_borda(fig, usar_borda=True, key="grafico", fullscreen_state_key="fullscreen"):
    html_fig = fig.to_html(full_html=False, include_plotlyjs='cdn')
    if st.session_state.get(fullscreen_state_key, False):
        st.plotly_chart(fig, use_container_width=True)
    elif usar_borda:
        border = get_border_config()
        components.html(f"""
            <div style="border: {border['width']} solid {border['color']}; border-radius: {border['radius']}; padding: 15px; margin-bottom: 20px;">
                {html_fig}
            </div>
        """, height=500)
    else:
        components.html(html_fig, height=500)

def grafico_barra_tipo(df, referencia):
    df = df.copy()
    df['Referência'] = pd.to_datetime(df['Referência']).dt.strftime('%Y-%m')
    df = df[df['Referência'] == referencia].drop(columns='Referência').T.reset_index()
    df.columns = ['Tipo', 'Quantidade']
    df = df.sort_values(by='Quantidade', ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Tipo'], y=df['Quantidade'], name=referencia,
        text=df['Quantidade'], textposition='auto', marker_color='blue'))
    fig.update_layout(
        title=f'Distribuição por Tipo de OS ({referencia})',
        xaxis_title='Tipo de OS', yaxis_title='Quantidade',
        xaxis_tickangle=-45, margin=dict(b=120), template='plotly_white')
    return fig

def grafico_percentual(df):
    df = df.copy()
    df['% Atendimento'] = np.where(df['OS Abertas'] > 0, (df['OS Atendidas'] / df['OS Abertas']) * 100, 0.0)
    df['Referência'] = pd.to_datetime(df['Referência']).dt.strftime('%m/%Y')
    df = df[['Referência', '% Atendimento']].sort_values('Referência')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Referência'], y=df['% Atendimento'], mode='lines+markers+text',
        name='% Atendimento', text=df['% Atendimento'].round(1).astype(str) + '%',
        textposition='top center'))
    fig.add_shape(type="line", x0=0, x1=1, xref='paper', y0=100, y1=100,
                  line=dict(color="red", width=2, dash="dash"))
    fig.update_layout(
        title='% Atendimento das OS', xaxis_title='Referência (Mês/Ano)',
        yaxis_title='Percentual (%)', xaxis=dict(tickangle=-45),
        hovermode='x unified', template='plotly_white')
    return fig

# Dashboard principal

def dashboard(df):
    st.markdown(titulo_page('Dashboard', ''), unsafe_allow_html=True)
    # -----------------------------------------------
    # Filtragem por Equipe
    equipe_opcao = st.sidebar.selectbox('Equipe', ['TODOS'] + sorted(df['EQUIPE'].dropna().unique(), reverse=True))
    if equipe_opcao != 'TODOS':
        df = df[df['EQUIPE'] == equipe_opcao]

    metricas_df = metricascorretivas(df)
    natureza_df = hist_natureza(df)
    tipo_df = hist_tipo(df)
    print(metricas_df)
    
    # Filtra por data do Mês
    for data in [metricas_df, natureza_df, tipo_df]:
        data['Referência'] = data['Referência'].astype(str)

    referencia_atual = st.sidebar.selectbox('Mês de Referência', sorted(metricas_df['Referência'].unique(), reverse=True))

    def obter_valor(df, ref, coluna):
        try:
            return df.loc[df['Referência'] == ref, coluna].values[0]
        except (IndexError, KeyError):
            return 0

    def calc_delta(atual, anterior):
        return int(atual - anterior)

    ano, mes = map(int, referencia_atual.split("-"))
    anterior = f"{ano - 1}-12" if mes == 1 else f"{ano}-{mes - 1:02d}"
    if anterior not in metricas_df['Referência'].values:
        anterior = referencia_atual

    st.text('Indicadores de Execução')
    colunas_exec = ['Backlogs', 'OS Abertas', 'OS Não Atendidas', 'OS Atendidas', 'Backlogs Atendidos']
    cols = st.columns(len(colunas_exec))
    for i, col in enumerate(colunas_exec):
        atual = obter_valor(metricas_df, referencia_atual, col)
        ant = obter_valor(metricas_df, anterior, col)
        cols[i].metric(col, atual, calc_delta(atual, ant))
    style_metric_cards(border_left_color='#FF8C00')

    st.text('Natureza de OS')
    natureza_cols = ['ACOMPANHAMENTO', 'CORRETIVA EMERGENCIAL', 'CORRETIVA PLANEJADA', 'OBRA E MELHORIA', 'PLANEJAMENTO'] 
    cols = st.columns(len(natureza_cols))
    for i, col in enumerate(natureza_cols):
        atual = obter_valor(natureza_df, referencia_atual, col)
        ant = obter_valor(natureza_df, anterior, col)
        cols[i].metric(col.title().replace('_', ' '), atual, calc_delta(atual, ant))


    
    # Opção de Utilizar Borda nos Gráficos
    usar_borda = st.sidebar.checkbox("Exibir bordas nos gráficos", value=True)
    if not usar_borda:
        st.sidebar.markdown(':blue[**⛶ Gráficos em tela cheia**]', unsafe_allow_html=True)
    st.session_state['fullscreen'] = not usar_borda
    print(df)
    # Exibir Gráficos
    col1, col2 = st.columns(2)
    with col1:
        exibir_com_borda(criar_grafico_linhas(metricas_df, ['OS Abertas', 'OS Atendidas', 'OS Não Atendidas', 'Backlogs'], 'OS Abertas vs Atendidas'), usar_borda)
        exibir_com_borda(criar_grafico_linhas(natureza_df, natureza_cols, 'Histórico de Natureza das OS'), usar_borda)
    with col2:
        exibir_com_borda(grafico_percentual(metricas_df), usar_borda)
        exibir_com_borda(criar_grafico_linhas(metricas_df.sort_values('Referência'), ['TME (h)', 'TMA (h)', 'TMS (h)'], 'Tempos Médios (Execução, Atendimento, Solução) em Horas'), usar_borda)

    exibir_com_borda(grafico_barra_tipo(tipo_df, referencia_atual), usar_borda)

if __name__ == "__main__":
    df = carregar_dados()
    dashboard(df)
