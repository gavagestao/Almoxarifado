import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Instaladora Pro - Gestão de Estoque", layout="wide")

# 2. DESIGN PERSONALIZADO (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetric"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        padding: 20px !important;
        border-radius: 12px !important;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }
    
    .badge-entrada {
        background-color: #dcfce7; color: #166534;
        padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 13px;
    }
    .badge-saida {
        background-color: #fee2e2; color: #991b1b;
        padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 13px;
    }
    
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 10px 0 !important; border-top: 1px solid #e2e8f0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE DADOS (PERSISTÊNCIA SIMPLES) ---
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Produto': 'Cabo Flexível 2.5mm', 'Categoria': 'Elétrica', 'Qtd': 100, 'Minimo': 500, 'Preco': 2.50},
        {'Produto': 'Tubo PVC 100mm', 'Categoria': 'Hidráulica', 'Qtd': 15, 'Minimo': 100, 'Preco': 45.00}
    ])

if 'movs' not in st.session_state:
    st.session_state.movs = pd.DataFrame(columns=['Tipo', 'Produto', 'Qtd', 'Motivo', 'Data'])

df = st.session_state.estoque
# Cálculos de segurança
df['Status_Critico'] = (df['Qtd'] <= (df['Minimo'] * 0.20))
df['Valor_Total'] = df['Qtd'] * df['Preco']

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>🏢 Almoxarifado</h2>", unsafe_allow_html=True)
    escolha = option_menu(
        menu_title=None,
        options=["Painel", "Produtos", "Movimentações"],
        icons=["grid-1x2", "box", "arrow-left-right"],
        default_index=0,
        styles={
            "container": {"background-color": "#0f172a"},
            "nav-link": {"color": "#94a3b8", "font-size": "15px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#1e293b", "color": "#f8fafc"},
        }
    )

# --- 5. LÓGICA DAS PÁGINAS ---

if escolha == "Painel":
    st.title("📊 Visão Geral da Obra")
    c1, c2, c3 = st.columns(3)
    
    patrimonio_total = df['Valor_Total'].sum()
    
    c1.metric("Itens Críticos", len(df[df['Status_Critico']]))
    c2.metric("Patrimônio Total", f"R$ {patrimonio_total:,.2f}")
    c3.metric("Saldo em Unidades", int(df['Qtd'].sum()))

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Distribuição de Estoque")
        fig = px.pie(df, values='Qtd', names='Categoria', hole=0.6
