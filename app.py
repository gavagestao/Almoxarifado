import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO E DESIGN
st.set_page_config(page_title="Gestão de Obra Pro", layout="wide")

# CSS Avançado para emular o estilo da imagem enviada
st.markdown("""
    <style>
    /* Fundo e Fonte */
    .main { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Barra de Busca e Filtros */
    .search-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        display: flex;
        gap: 10px;
    }

    /* Estilo dos Cards de Métrica */
    div[data-testid="stMetric"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        padding: 20px !important;
        border-radius: 12px !important;
    }

    /* Badges de Entrada/Saída */
    .badge-entrada {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-saida {
        background-color: #ffedd5;
        color: #9a3412;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] { background-color: #0f172a; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS (Simulado para este exemplo) ---
if 'movimentacoes' not in st.session_state:
    st.session_state.movimentacoes = pd.DataFrame([
        {'Tipo': 'Entrada', 'Produto': 'Parafuso Phillips 6mm', 'Qtd': 200, 'Motivo': 'Compra fornecedor', 'Data': '31/10/2024'},
        {'Tipo': 'Saída', 'Produto': 'Luva de Procedimento M', 'Qtd': 5, 'Motivo': 'Uso setor produção', 'Data': '04/11/2024'},
        {'Tipo': 'Entrada', 'Produto': 'Fita Isolante Preta', 'Qtd': 15, 'Motivo': 'Reposição estoque', 'Data': '09/11/2024'},
        {'Tipo': 'Saída', 'Produto': 'Capacete de Segurança', 'Qtd': 2, 'Motivo': 'Entrega novos funcionários', 'Data': '11/11/2024'}
    ])

# --- MENU LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>🏢 Almoxarifado</h2>", unsafe_allow_html=True)
    escolha = option_menu(
        menu_title=None,
        options=["Painel", "Produtos", "Movimentações"],
        icons=["grid-1x2", "box", "arrow-left-right"],
        default_index=2, # Começa na página que você mostrou
        styles={
            "container": {"background-color": "#0f172a"},
            "nav-link": {"color": "#94a3b8", "font-size": "15px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#1e293b", "color": "#f8fafc"},
        }
    )

# --- PÁGINA DE MOVIMENTAÇÕES (O modelo da imagem) ---
if escolha == "Movimentações":
    col_t1, col_t2 = st.columns([8, 2])
    with col_t1:
        st.title("Movimentações")
    with col_t2:
        st.write("") # Espaçador
        if st.button("+ Nova Movimentação", use_container_width=True, type="primary"):
            st.toast("Função de cadastro abrirá aqui!")

    # Barra de busca e Filtro
    c_search, c_filter = st.columns([9, 1])
    busca = c_search.text_input("🔍 Buscar por produto...", label_visibility="collapsed")
    c_filter.button("⚙️ Filtros")

    # Tabela Estilizada
    st.markdown("---")
    
    # Cabeçalho da Tabela
    h1, h2, h3, h4, h5 = st.columns([1.5, 3.5, 1, 3, 2])
    h1.caption("Tipo")
    h2.caption("Produto")
    h3.caption("Qtd.")
    h4.caption("Motivo / Destino")
    h5.caption("Data")

    # Linhas da Tabela
    for index, row in st.session_state.movimentacoes.iterrows():
        if busca.lower() in row['Produto'].lower():
            r1, r2, r3, r4, r5 = st.columns([1.5, 3.5, 1, 3, 2])
            
            # Badge de Tipo
            if row['Tipo'] == 'Entrada':
                r1.markdown(f'<span class="badge-entrada">● Entrada</span>', unsafe_allow_html=True)
            else:
                r1.markdown(f'<span class="badge-saida">● Saída</span>', unsafe_allow_html=True)
            
            r2.markdown(f"**{row['Produto']}**")
            r3.write(row['Qtd'])
            r4.write(row['Motivo'])
            r5.write(row['Data'])
            st.markdown("<hr style='margin:5px 0; border-color:#f1f5f9'>", unsafe_allow_html=True)

# --- DEMAIS PÁGINAS (Simuladas) ---
elif escolha == "Painel":
    st.title("Dashboard
