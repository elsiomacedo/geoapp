import streamlit as st
import streamlit_javascript as st_javascript
from config import *

def load_css():
    """Carrega o conteúdo do arquivo CSS.

    Returns:
        str: Conteúdo CSS ou comentário de erro.
    """
    try:
        with open(APP_CSS_STYLE) as f:
            return f.read()
    except FileNotFoundError:
        return "/* CSS file not found */"
    
def detectar_tema():
    """
    Detecta o tema atual (claro ou escuro) em uma aplicação Streamlit.
    Este método injeta um elemento HTML oculto no DOM com a cor de fundo do tema atual
    e utiliza JavaScript para obter a cor computada. Com base na cor RGB obtida, 
    determina se o tema é escuro ou claro.
    Returns:
        str: "dark" se o tema for escuro, "light" se o tema for claro.
    """
    # Injeta um div oculto com a cor de fundo do tema atual
    st.markdown("""
        <div id="theme-detector" style="background-color: var(--background-color); display:none;"></div>
    """, unsafe_allow_html=True)

    # JavaScript pega a cor computada do background

    cor_fundo = st_javascript(""" 
        const elem = window.parent.document.getElementById("theme-detector");
        const color = window.getComputedStyle(elem).backgroundColor;
        color;
    """)

    # Analisa se é tema escuro baseado na cor RGB
    if cor_fundo and isinstance(cor_fundo, str):
        if "rgb(0, 0, 0" in cor_fundo or "rgb(1, 1, 1" in cor_fundo:  # preto ou quase preto
            return "dark"
        else:
            return "light"
    return "light"  # fallba

def _ajustar_sidebar() -> None:
    """Ajusta o estilo da barra lateral."""
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

    _ajustar_sidebar()

    tema = detectar_tema()
    marca = LOGO_LIGHT if tema == 'light' else LOGO_DARK
    st.logo(marca, size="large", icon_image=LOGO_ICON)

def aplicar_estilos():
    """Aplica estilos CSS e cabeçalho da página."""
    st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">',
        unsafe_allow_html=True)    