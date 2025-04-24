import streamlit as st
from utils.mt_card import mt_card

# USO NO APP
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
        hover_color="#000000"
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