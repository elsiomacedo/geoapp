import plotly.express as px

def grafico_tempo_medio(df, tipo='TECNICO'):
    """
    Gera um gráfico de barras com o tempo médio por técnico, equipe ou tipo.
    """
    df_medias = df.groupby(tipo)['Tempo_min'].mean().reset_index()
    fig = px.bar(df_medias, x=tipo, y='Tempo_min', title=f'Tempo Médio por {tipo}')
    fig.update_layout(
        xaxis_title=tipo,
        yaxis_title='Tempo Médio (min)',
        title_x=0.5
    )
    return fig