import streamlit as st
from streamlit.components.v1 import html

def format_brazilian_number(value):
    """Formata números no padrão brasileiro: 1.234,56"""
    try:
        num = float(value)
        if num.is_integer():
            return f"{int(num):,}".replace(",", ".")
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return str(value)
def mt_card(
    title,
    current_value,
    previous_value,
    stripe_color="#FFA500",
    height=130,  # Altura fixa em 120px
    icon_name="insights",
    history=None,
    bar_color="#8884d8",
    theme="light",
    hover_color="#F5F5F5"
):
    # Configuração de cores baseada no tema
    if history==None:
        height = 90  # Altura reduzida se não houver histórico
    else:
        height = 115
    
    bg_color = "#1E1E1E" if theme == "dark" else "#FFFFFF"
    text_color = "#FFFFFF" if theme == "dark" else "#000000"
    subtext_color = "#AAAAAA" if theme == "dark" else "#555555"
    border_color = "#333333" if theme == "dark" else "#E0E0E0"
    
    # Formatando os valores
    formatted_current = format_brazilian_number(current_value)
    formatted_previous = format_brazilian_number(previous_value)
    
    # Cálculos de variação
    delta = current_value - previous_value
    delta_pct = (delta / previous_value * 100) if previous_value != 0 else 0
    delta_icon = "arrow_upward" if delta >= 0 else "arrow_downward"
    delta_clr = "#4CAF50" if delta >= 0 else "#F44336"
    formatted_delta = format_brazilian_number(abs(delta))
    
    # Gráfico com largura máxima e design aprimorado
    bar_svg = ""
    chart_height = 28  # Altura padrão do gráfico
    chart_wrapper_style = "min-height: 0px;"  # Estilo padrão sem gráfico
    
    if history and len(history) > 0:
        max_val = max(history) or 1
        total_bars = len(history)
        bar_width = 16  # Barras mais largas
        bar_spacing = 4  # Espaçamento equilibrado
        total_width = total_bars * (bar_width + bar_spacing)
        
        bar_svg = f'''
        <div style="margin-top: 2px; width: 100%; overflow: hidden;">
            <svg width="{total_width}px" height="{chart_height}" viewBox="0 0 {total_width} {chart_height}">
        '''
        for i, val in enumerate(history):
            bar_height = (val / max_val) * (chart_height - 2)
            x_pos = i * (bar_width + bar_spacing)
            y_pos = chart_height - bar_height
            bar_svg += f'''
            <rect x="{x_pos}" y="{y_pos}" 
                  width="{bar_width}" height="{bar_height}" 
                  fill="{bar_color}" rx="3"
                  style="transition: all 0.3s ease;">          
                <title>Valor: {format_brazilian_number(val)}</title>
            </rect>
            '''
        bar_svg += '</svg></div>'
        chart_wrapper_style = f"min-height: {chart_height}px;"  # Ajusta altura quando há gráfico
    
    # HTML com layout ultra-otimizado
    html_content = f"""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        .metric-card {{
            position: relative;
            height: {height}px;
            background: {bg_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            margin: 6px 0;
            padding-left: 8px;
            transition: all 0.3s ease;
            font-family: 'Segoe UI', Roboto, sans-serif;
            box-sizing: border-box;
            overflow: hidden;
        }}
        .metric-card:hover {{
            background: {hover_color};
            cursor: pointer;
            transform: translateY(-5px);
            box-shadow: 3px 3px 20px rgba(0,0,0,0.2); /* Aumentando a sombra */
        }}
        .stripe {{
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 8px;
            height: 100%;
            background: {stripe_color};
            border-radius: 8px 0 0 8px;
        }}
        .card-content {{
            height: 100%;
            padding: 8px 10px 8px 0px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;            
            box-sizing: border-box;
        }}
        .metric-title {{
            color: {subtext_color};
            font-size: 14px;
            font-weight: 500;
             white-space: nowrap;
        }}
        .metric-value {{
            color: {text_color};
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        .delta-container {{
            display: flex;
            align-items: center;
            gap: 4px;
            margin: 3px 0;
        }}
        .delta-value {{
            color: {delta_clr};
            font-size: 12px;
            font-weight: 500;
        }}
        .chart-wrapper {{
            flex-grow: 1;
            {chart_wrapper_style}
            width: 100%;
            overflow: hidden;
        }}
        .material-icons {{
            font-size: 20px !important;
            vertical-align: middle;
        }}
    </style>
    
    <div class="metric-card">
        <div class="stripe"></div>
        <div class="card-content">
            <div style="position: absolute; right: 6px; color: {subtext_color};">
                <i class="material-icons">{icon_name}</i>
            </div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{formatted_current}</div>
            <div class="delta-container">
                <i class="material-icons" style="color: {delta_clr}">{delta_icon}</i>
                <span class="delta-value">{formatted_delta} ({delta_pct:+.1f}%)</span>
            </div>
            <div class="chart-wrapper">
                {bar_svg}
            </div>
        </div>
    </div>
    """
    
    html(html_content, height=height+10)

# Dashboard de demonstração
st.title("Dashboard de Métricas Otimizadas")

row1 = st.columns(3)
row2 = st.columns(3)

with row1[0]:
    mt_card(
        "Vendas Brutas", 
        125678.50, 
        112345.75,
        stripe_color="#2196F3",
        icon_name="attach_money",
        history=[112345, 115678, 80000, 123456, 124000, 125678, 123400, 126500],
        bar_color="#BBDEFB"
    )

with row1[1]:
    mt_card(
        "Novos Clientes",
        342,
        298,
        stripe_color="#4CAF50",
        icon_name="person_add",
        history=[298, 310, 325, 330, 335, 342, 338, 345],
        bar_color="#C8E6C9"
    )

with row1[2]:
    mt_card(
        "Ticket Médio (R$)",
        89.50,
        85.25,
        stripe_color="#9C27B0",
        icon_name="shopping_cart",
        history=[85.25, 86.00, 87.30, 88.15, 88.90, 89.50, 88.75, 90.00],
        bar_color="#E1BEE7"
    )

with row2[0]:
    mt_card(
        "Churn Rate",
        5.2,
        6.8,
        stripe_color="#FF5722",
        icon_name="trending_down",
        history=[6.8, 6.5, 6.2, 5.9, 5.7, 5.5, 5.3, 5.2],
        bar_color="#FFCCBC"
    )

with row2[1]:
    mt_card(
        "Satisfação (NPS)",
        78,
        72,
        stripe_color="#FFC107",
        icon_name="sentiment_satisfied",
        history=[72, 73, 74, 75, 76, 77, 77, 78],
        bar_color="#FFECB3"
    )

with row2[2]:
    mt_card(
        "Produtividade",
        92.5,
        89.3,
        stripe_color="#00BCD4",
        icon_name="speed",
        history=[89.3, 90.1, 90.8, 91.2, 91.7, 92.1, 92.3, 92.5],
        bar_color="#B2EBF2",
        theme="dark"
    )
col1, col2 = st.columns(2)

with col1:
    mt_card(
        "Erros do Sistema",
        5,
        8,
        stripe_color="#E53935",
        icon_name="bug_report",
        history=[8, 6, 7, 5, 4, 5],
        bar_color="#FFCDD2",
        theme="light",
        hover_color="#FFEBEE"
    )

with col2:
    mt_card(
        "Tarefas Concluídas",
        23,
        15,
        stripe_color="#4CAF50",
        icon_name="check_circle",
        history=[15, 18, 20, 19, 22, 23],
        bar_color="#C8E6C9",
        theme="light",
        hover_color="#E8F5E9"
    )

# Card sem gráfico para demonstrar a tarja
mt_card(
    "Alertas de Segurança",
    3,
    2,
    stripe_color="#FFC107",
    icon_name="warning",
    theme="light",
    hover_color="#C0C0C0"
)