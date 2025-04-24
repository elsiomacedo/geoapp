from components import exibir_aggrid
import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
from components import titulo_page
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.tools import aggrid_ptbr, remover_acentos

PORTUGUESE_TEXTS = aggrid_ptbr()

def aplicar_filtros_textuais(df, palavras):
    palavras_sem_acento = [remover_acentos(p).lower().strip() for p in palavras]
    aplicar_filtro_status = "nao atendida" in palavras_sem_acento
    palavras_sem_acento = [p for p in palavras_sem_acento if p != "nao atendida"]

    df_sem_acento = df.astype(str).map(remover_acentos)
    mascara = pd.Series(True, index=df.index)

    if palavras_sem_acento:
        mascara_texto = df_sem_acento.apply(
            lambda row: all(p in ' '.join(row).lower() for p in palavras_sem_acento),
            axis=1
        )
        mascara &= mascara_texto

    if aplicar_filtro_status and "STATUS" in df.columns:
        mascara &= df["STATUS"].astype(str).str.upper() != "ATENDIDO"

    return df[mascara]

def carregar_dados(caminho_csv):
    try:
        df = pd.read_csv(caminho_csv, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# ================================
# APLICATIVO STREAMLIT
# ================================

def tecnicos():
    st.markdown(titulo_page('Equipe Técnica', 'Produtividade Mês Atual'), unsafe_allow_html=True)
    df = carregar_dados('dados/DBTecno_All.csv')
    if df.empty:
        return

    opcoes_referencia = ['TODOS'] + sorted(df['Referência'].unique(), reverse=True)
    referencia_atual = st.sidebar.selectbox(
        'Referência',
        opcoes_referencia,
        index=1 if len(opcoes_referencia) > 1 else 0
    )

    if referencia_atual != 'TODOS':
        df['Início-n'] = pd.to_datetime(df['Início']).dt.strftime('%Y-%m')
        df['Término-n'] = pd.to_datetime(df['Término']).dt.strftime('%Y-%m')
        df = df[(df['Início-n'] == referencia_atual) | (df['Término-n'] == referencia_atual)]

    colunas_visiveis = ['TECNICO', 'EQUIPE', 'TIPO', 'Nº OS', 'Início', 'Término', 'Tempo']
    df = df[colunas_visiveis]

    if 'filtro_status' not in st.session_state:
        st.session_state.filtro_status = []

    titulo_expander = "Filtros (**Aplicados**) e Visibilidade dos Campos ╰┈➤" if st.session_state.filtro_status else "Filtros e Visibilidade dos Campos ╰┈➤"
    with st.expander(titulo_expander):
        palavras = st_tags(
            label='Digite Palavras para aplicar Filtros',
            text='Enter para adicionar',
            value=[],
            maxtags=10,
            key="filtro_status"
        )
        if palavras:
            df = aplicar_filtros_textuais(df, palavras)

    aba1, aba2 = st.tabs(['Execução da Equipe', 'Indicadores de Produtividade'])

    with aba1:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True, filter=True, sortable=True)
        gb.configure_selection('multiple', use_checkbox=False)
        grid_options = gb.build()
        grid_options['localeText'] = PORTUGUESE_TEXTS

        AgGrid(
            df,
            localeText=PORTUGUESE_TEXTS,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            use_container_width=True,
            height=300
        )

    with aba2:
        st.info("Indicadores em desenvolvimento.")

if __name__ == "__main__":
    tecnicos()