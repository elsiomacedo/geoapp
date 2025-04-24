import pandas as pd


def hist_natureza(df):
    # Criar coluna com mês referência
    df["Referência"] = df["Data/Hora Abertura"].dt.to_period("M").dt.strftime("%Y-%m").sort_values()
    #meses = df["Referência"].dropna().unique()

    # Novo DataFrame por Natureza de OS
    df_natureza = df.groupby(["Referência", "NATUREZA"]).size().unstack(fill_value=0).reset_index()
    df_natureza.index.name = None  # remove o nome do índice    
    return df_natureza

def hist_tipo(df):
    df = df.copy()
   
    # Criar coluna com mês referência
    df["Referência"] = df["Data/Hora Abertura"].dt.to_period("M").dt.strftime("%Y-%m")
    df = df.sort_values("Referência")    
    #meses = df["Referência"].dropna().unique()

    # Novo DataFrame por Tipo de OS
    df_tipo = df.groupby(["Referência", "TIPO DE OS"]).size().unstack(fill_value=0).reset_index()
    df_tipo.index.name = None  # remove o nome do índice 
    return df_tipo


def metricascorretivas(df):
    df = df.copy()
    # Criar coluna com mês referência
    df["Mês Referência"] = df["Data/Hora Abertura"].dt.to_period("M").dt.strftime("%Y/%m").sort_values()
    meses = df["Mês Referência"].dropna().unique()

    resultados = []

    for mes in meses:
        inicio = pd.Timestamp(mes + "-01")
        fim = inicio + pd.offsets.MonthEnd(0)
        df_mes = df[df["Mês Referência"] == mes]

        os_abertas = len(df_mes)
        os_atendidas = df_mes["Data/Hora Término"].notna().sum()
        os_nao_atendidas = os_abertas - os_atendidas

        backlog = df[(df["Data/Hora Abertura"] < inicio) & (df["Data/Hora Término"].isna())].shape[0]
        backlog_atendidos = df[(df["Data/Hora Abertura"] < inicio) &
                               (df["Data/Hora Término"] >= inicio) &
                               (df["Data/Hora Término"] <= fim)].shape[0]

        df_exec = df_mes[df_mes["Data/Hora Início"].notna() & df_mes["Data/Hora Término"].notna()].copy()
        df_exec["TME (h)"] = (df_exec["Data/Hora Término"] - df_exec["Data/Hora Início"]).dt.total_seconds() / 3600
        df_exec["TMA (h)"] = (df_exec["Data/Hora Início"] - df_exec["Data/Hora Abertura"]).dt.total_seconds() / 3600
        df_exec["TMS (h)"] = (df_exec["Data/Hora Término"] - df_exec["Data/Hora Abertura"]).dt.total_seconds() / 3600

        tme = df_exec["TME (h)"].mean()
        tma = df_exec["TMA (h)"].mean()
        tms = df_exec["TMS (h)"].mean()

        resultados.append({
            "Referência": inicio.strftime("%Y-%m"),
            "Backlogs": backlog,
            "OS Abertas": os_abertas,
            "OS Não Atendidas": os_nao_atendidas,
            "OS Atendidas": os_atendidas,
            "Backlogs Atendidos": backlog_atendidos,
            "TME (h)": round(tme, 2),
            "TMA (h)": round(tma, 2),
            "TMS (h)": round(tms, 2)
        })

    df_resultados = pd.DataFrame(resultados)
    df_resultados["% Atendimento"] = ((df_resultados["OS Atendidas"] / df_resultados["OS Abertas"]) * 100).round(1)

    return df_resultados