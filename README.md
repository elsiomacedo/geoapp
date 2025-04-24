# 📊 AppGeop - Indicadores de Manutenção

Este é um aplicativo desenvolvido em **Python + Streamlit** com foco na visualização de dados de manutenção, utilizando dados extraídos do sistema Optimus.

## 🚀 Funcionalidades

- Autenticação e navegação por páginas
- Indicadores de manutenção com gráficos interativos (Plotly)
- Tabelas responsivas com AgGrid
- Filtros por técnico, tipo, natureza, área e período
- Referência temporal padrão (aaaa-mm)
- Layout adaptado para tema claro/escuro
- Estrutura modular para fácil manutenção

## 📁 Estrutura do Projeto

```
appgeop/
├── app_pages/              # Páginas do Streamlit
├── dados/                  # Arquivos CSV e Excel
├── imgs/                   # Logotipos
├── utils/                  # Funções auxiliares e gráficos
├── components.py           # Interface visual (cards, AgGrid, métricas)
├── config.py               # Constantes globais e caminhos
├── geoapp.py               # Arquivo principal do app
```

## ⚙️ Requisitos

- Python 3.9+
- Streamlit
- streamlit-aggrid
- pandas, plotly, openpyxl

## ▶️ Como executar

```bash
# Instale dependências
pip install -r requirements.txt

# Rode o aplicativo
streamlit run appgeop/geoapp.py
```

## 📦 Versões refatoradas por etapa

Cada etapa implementa uma melhoria:
- Etapa 1–2: Organização e centralização de configurações
- Etapa 3–4: Modularização de gráficos e filtros
- Etapa 5–6: Leitura de dados e visualização com AgGrid
- Etapa 7–8: Referência temporal + layout organizado
- Etapa 9: Refinamento estético (ícones, containers)

---

Desenvolvido por [Elsio](mailto:elsio@example.com) ⚡