import streamlit as st
from streamlit.components.v1 import html
from utils.tools import format_brazilian_number

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