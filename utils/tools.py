
"""
tools_refatorado.py

Módulo unificado com funções organizadas em seções lógicas:
- Tempo e Horário
- Formatação
- Manipulação de Dados
- Streamlit
- AG Grid
- Arquivos
"""

# ===============================
# ⏱ TEMPO E HORÁRIO
# -------------------------------
# - `tempo_para_minutos`
# - `minutos_para_hhhmm`
# - `parse_time`
# - `combinar_data_hora`
# - `calcular_tempo`
# ===============================
import pandas as pd
from datetime import datetime
from typing import Optional
import unicodedata
import time
from pathlib import Path
import streamlit as st

def tempo_para_minutos(tempo: str) -> int:
    """Converte tempo no formato 'HH:MM' para minutos inteiros."""
    horas, minutos = map(int, tempo.split(':'))
    return horas * 60 + minutos

def minutos_para_hhhmm(minutos: float | int) -> str:
    """Converte minutos inteiros para o formato 'HHH:MM'."""
    if pd.isna(minutos): return "000:00"
    h = int(minutos // 60)
    m = int(minutos % 60)
    return f"{h:03}:{m:02}"

def parse_time(time_str: str) -> Optional[datetime.time]:
    """Converte string de hora em datetime.time."""
    if not time_str or pd.isnull(time_str):
        return None
    for fmt in ('%H:%M:%S', '%H:%M'):
        try:
            return pd.to_datetime(time_str, format=fmt).time()
        except ValueError:
            continue
    return None

def combinar_data_hora(data_col, hora_col) -> pd.Series:
    return pd.to_datetime(
        data_col.dt.strftime('%d/%m/%Y') + ' ' +
        hora_col.apply(lambda t: t.strftime('%H:%M:%S') if t else "00:00:00"),
        format='%d/%m/%Y %H:%M:%S'
    )

def calcular_tempo(delta) -> Optional[str]:
    if not isinstance(delta, pd.Timedelta) or pd.isnull(delta):
        return None
    total_seconds = delta.total_seconds()
    horas = int(total_seconds // 3600)
    minutos = int((total_seconds % 3600) // 60)
    return f"{horas:03}:{minutos:02}"


# ===============================
# 🧹 Formatação
# -------------------------------
# - `remover_acentos`
# - `format_brazilian_number`
# ===============================

def remover_acentos(texto):
    """Remove acentuação de strings."""
    if isinstance(texto, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    return texto

def format_brazilian_number(value):
    """Formata números no padrão brasileiro: 1.234,56"""
    try:
        num = float(value)
        if num.is_integer():
            return f"{int(num):,}".replace(",", ".")
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(value)


# ===============================
# 🧾 Manipulação de Dados
# -------------------------------
# - `carregar_dados_csv`
# - `carregar_dados_excel`
# - `preparar_datas`
# - `gerar_referencia`
# - `filtrar_por_referencia`
# - `gravacsv`
# ===============================

def carregar_dados_csv(caminho, parse_dates=None):
    """Carrega arquivo CSV com tratamento opcional de datas."""
    return pd.read_csv(caminho, parse_dates=parse_dates)

def carregar_dados_excel(caminho, parse_dates=None, sheet_name=0):
    """Carrega arquivo Excel com tratamento opcional de datas."""
    df = pd.read_excel(caminho, sheet_name=sheet_name)
    if parse_dates:
        for col in parse_dates:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
    return df  

def preparar_datas(df):
    df = df.copy()
    df["Data/Hora Abertura"] = pd.to_datetime(df["Data/Hora Abertura"], errors='coerce')
    df["Data/Hora Início"] = pd.to_datetime(df["Data/Hora Início"], errors='coerce')
    df["Data/Hora Término"] = pd.to_datetime(df["Data/Hora Término"], errors='coerce')
    df["Referência"] = df["Data/Hora Abertura"].dt.to_period("M").dt.strftime("%Y-%m")
    return df.sort_values("Referência")

def gerar_referencia(df, coluna_data, nome_coluna="Referência"):
    """Cria coluna 'Referência' no formato 'aaaa-mm' com base em uma coluna de datas."""
    df[nome_coluna] = pd.to_datetime(df[coluna_data], errors='coerce').dt.to_period("M").astype(str)
    return df

def filtrar_por_referencia(df, referencia, coluna="Referência"):
    """Filtra o DataFrame com base na referência fornecida (aaaa-mm)."""
    return df[df[coluna] == referencia]

def gravacsv(df: pd.DataFrame, output_file_name: str):
    df.to_csv(f'dados/{output_file_name}', index=False, encoding='utf-8')


# ===============================
# 🖼️ Streamlit Utilities
# -------------------------------
# - `detectar_tema`
# - `criar_select_filtro`
# - `criar_multiselect_filtro`
# ===============================

def detectar_tema():
    from streamlit_javascript import st_javascript
    return st_javascript("window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'")

def criar_select_filtro(df, coluna, label, incluir_todos=True):
    opcoes = sorted(df[coluna].dropna().unique().tolist())
    if incluir_todos:
        opcoes = ["Todos"] + opcoes
    selecao = st.selectbox(label, opcoes)
    if selecao != "Todos":
        df = df[df[coluna] == selecao]
    return df, selecao

def criar_multiselect_filtro(df, coluna, label):
    opcoes = sorted(df[coluna].dropna().unique().tolist())
    selecao = st.multiselect(label, opcoes, default=opcoes)
    df = df[df[coluna].isin(selecao)]
    return df, selecao


# ===============================
# 🌍 AG Grid em Português
# -------------------------------
# - `aggrid_ptbr`
# ===============================

def aggrid_ptbr():
    return {
        "page": "Página",
        "more": "Mais",
        "to": "até",
        "of": "de",
        "next": "Próximo",
        "last": "Último",
        "first": "Primeiro",
        "previous": "Anterior",
        "loadingOoo": "Carregando...",
        "selectAll": "Selecionar Todos",
        "searchOoo": "Buscar...",
        "blanks": "Em branco",
        "filterOoo": "Filtrar...",
        "applyFilter": "Aplicar filtro...",
        "equals": "Igual",
        "notEqual": "Diferente",
        "contains": "Contém",
        "notContains": "Não contém",
        "startsWith": "Começa com",
        "endsWith": "Termina com",
        "andCondition": "E",
        "orCondition": "Ou",
        "group": "Grupo",
        "columns": "Colunas",
        "filters": "Filtros",
        "rowGroupColumnsEmptyMessage": "Arraste colunas aqui para agrupar",
        "valueColumnsEmptyMessage": "Arraste aqui para agregar",
        "noRowsToShow": "Nenhuma linha para exibir",
        "pinColumn": "Fixar Coluna",
        "valueAggregation": "Agregação de Valor",
        "autosizeThiscolumn": "Autoajustar esta Coluna",
        "autosizeAllColumns": "Autoajustar Todas Colunas",
        "groupBy": "Agrupar por",
        "ungroupBy": "Desagrupar por",
        "resetColumns": "Redefinir Colunas",
        "export": "Exportar",
        "csvExport": "Exportar para CSV",
        "excelExport": "Exportar para Excel (.xlsx)",
        "pinLeft": "Fixar à esquerda",
        "pinRight": "Fixar à direita",
        "noPin": "Não fixar",
        "copy": "Copiar",
        "copyWithHeaders": "Copiar com cabeçalhos",
        "copyWithGroupHeaders": "Copiar com cabeçalhos de grupo",
        "paste": "Colar",
        "autoSizeThis": "Ajustar automaticamente esta coluna",
        "autoSizeAll": "Ajustar automaticamente todas",
        "sortAscending": "Ordenar ascendente",
        "sortDescending": "Ordenar descendente",
        "noSort": "Sem ordenação",
        "menu": "Menu",
        "hideColumn": "Ocultar coluna"
    }

# ===============================
# 📁 Arquivos
# -------------------------------
# - `load_excel`
# - `last_access`
# ===============================

def load_excel(file_name: str) -> Optional[pd.DataFrame]:
    file_path = Path('dados') / file_name
    try:
        xls = pd.ExcelFile(file_path)
        df = xls.parse(xls.sheet_names[0], header=6)
        return df.iloc[:-1].reset_index(drop=True)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo '{file_name}': {e}")
        return None

def last_access(file_name: str) -> str:
    caminho_arquivo = Path('dados') / file_name
    return time.strftime('%d/%m/%Y', time.localtime(caminho_arquivo.stat().st_mtime))
