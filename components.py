from PIL import Image
import base64
import streamlit as st
from config import APP_TITLE, APP_ICON, SIDEBAR_INIT, LOGO_DARK, LOGO_LIGHT, LOGO_ICON
import streamlit as st
#from config import APP_TITLE, APP_ICON, SIDEBAR_INIT, LOGO_DARK, LOGO_LIGHT, LOGO_ICON
from utils.tools import detectar_tema

def get_image_base64(image_path):
    """
        Função para converter imagem local para base64'
    """    
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
def load_css():
    """
        Função para carregar Arquivo CSS
    """    
    try:
        with open("/style/header.css") as f:
            return f.read()
    except FileNotFoundError:
        return "/* CSS file not found */"
def header_page(Texto):
    """
        Função para retornae o cabeçalho da página
    """    
    return f"""
    <div style=" margin-top: -140px; margin-bottom: -5px;">
            <h2 style="font-weight: bold; line-height: 1;">{Texto}</h2>      
    </div>
    <hr style="margin-top: -10px; margin-bottom: 10px; border: 1px solid #ccc;">
    """  
def titulo_page(titulo, subtitulo):
    """
        Função para retornae o cabeçalho da página
    """    
    return f"""
    <div style=" margin-top: -50px; margin-bottom: 10px"">
            <h3 style="margin-bottom: -10px; line-height: 1;">{titulo}</h3>      
            <p style="line-height: 1">{subtitulo}</p>               
    </div>
    """  
def header_side():
    """
        Função para retornar o cabeçalho da barra lateral
    """    
    return f"""
        <div>
            <h3 class="header_side">GEOP Gerência Operacional</h3>
            <p class="header_side">Aplicando IA no sistema OPTIMUS</p>        
             <hr class="hr">
        </div>
    """    
def footer_page():
    return """
    <div class="footer">
        <p>© 2025, GEOP Todos os direitos reservados.</p>
    </div>
    """

def sidebar_component():
    return """
    <div class="sidebar">
        <h4>Menu</h4>
        <ul>
            <li><a href="#">Item 1</a></li>
            <li><a href="#">Item 2</a></li>
            <li><a href="#">Item 3</a></li>
        </ul>
    </div>
    """


def configurar_pagina():
    """
    Configura a página principal do Streamlit, incluindo título, layout e logotipo
    baseado no tema claro ou escuro.
    """
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        initial_sidebar_state=SIDEBAR_INIT,
        layout="wide"
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 250px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    tema = detectar_tema()
    marca = LOGO_LIGHT if tema == 'light' else LOGO_DARK
    st.logo(marca, size="large", icon_image=LOGO_ICON)

import streamlit as st

def exibir_metrica(label, valor, delta=None, help_text=None):
    """
    Exibe um cartão de métrica padronizado com rótulo, valor e delta opcional.
    """
    st.metric(label=label, value=valor, delta=delta, help=help_text)

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import streamlit as st

def exibir_aggrid(df, height=400, fit_columns=True, selection_mode="single", use_container_width=True):
    """
    Exibe um DataFrame utilizando AgGrid com configurações padronizadas.
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode=selection_mode, use_checkbox=True)
    
    if fit_columns:
        gb.configure_grid_options(domLayout='normal', autoHeight=True)

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=height,
        use_container_width=use_container_width,
        fit_columns_on_grid_load=fit_columns
    )
    return grid_response

def container_metricas(titulo, metricas: list):
    """
    Exibe um conjunto de métricas em colunas com título opcional.
    metricas = [(label, valor, delta), ...]
    """
    if titulo:
        st.markdown(f"### {titulo}")

    cols = st.columns(len(metricas))
    for col, (label, valor, delta) in zip(cols, metricas):
        with col:
            exibir_metrica(label, valor, delta)