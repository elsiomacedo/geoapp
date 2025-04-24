import streamlit as st
import time
from components import configurar_pagina, header_page
from streamlit_javascript import st_javascript
from utils.tools_ui import aplicar_estilos
from config import APP_TITLE, APP_ICON, SIDEBAR_INIT, LOGO_DARK, LOGO_LIGHT, LOGO_ICON

#def detectar_tema():
#    # Injeta um div oculto com a cor de fundo do tema atual
#    st.markdown("""
#        <div id="theme-detector" style="background-color: var(--background-color); display:none;"></div>
#    """, unsafe_allow_html=True)
#
#    # JavaScript pega a cor computada do background
#    cor_fundo = st_javascript("""
#        const elem = window.parent.document.getElementById("theme-detector");
#        const color = window.getComputedStyle(elem).backgroundColor;
#        color;
#    """)
#    # Analisa se é tema escuro baseado na cor RGB
#    if cor_fundo and isinstance(cor_fundo, str):
#        if "rgb(0, 0, 0" in cor_fundo or "rgb(1, 1, 1" in cor_fundo:  # preto ou quase preto
#            return "dark"
#        else:
#            return "light"
#    return "light"  # fallback


def carregar_paginas():
    """Define a estrutura de navegação entre as páginas da aplicação."""
    paginas = {
        "": [
            st.Page('app_pages/dashboard.py', title='Dashboard Geral', icon=':material/monitoring:'),
        ],
        "Ordens de Serviços": [
            st.Page('app_pages/corretivas.py', title='OS Corretivas', icon=':material/docs:'),
            st.Page('app_pages/tecnicos.py', title='Produtividade', icon=':material/group:'),
        ],
        "Mobile": [
            st.Page('app_pages/mb_corretivas.py', title='Corretivas', icon=':material/phone_iphone:'),
            st.Page('app_pages/graph.py', title='GRAPH', icon=':material/phone_iphone:'),            
        ],        
        "Configurações": [
            st.Page('app_pages/atualdata.py', title='Atualiza Dados', icon=':material/database:'),
        ],
    }
    return st.navigation(paginas, position='sidebar')



def main():
    configurar_pagina()
    aplicar_estilos()
    st.markdown(header_page('Gestão de Operações'), unsafe_allow_html=True)    
    pagina = carregar_paginas()
    pagina.run()

if __name__ == '__main__':
    main()
