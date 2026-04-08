import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Instaladora Pro", layout="wide")

# 2. ESTILO CSS
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetric"] { background-color: white !important; border: 1px solid #e2e8f0 !important; padding: 20px !important; border-radius: 12px !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }
    .badge-entrada { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; }
    .badge-saida { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 10px 0 !important; border-top: 1px solid #e2e8f0 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DADOS EM MEMÓRIA
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Produto': 'Cabo Flexível 2.5mm', 'Categoria': 'Elétrica', 'Qtd': 100, 'Minimo': 500, 'Preco': 2.50},
        {'Produto': 'Tubo PVC 100mm', 'Categoria': 'Hidráulica', 'Qtd': 15, 'Minimo': 100, 'Preco': 45.00}
    ])

if 'movs' not in st.session_state:
    st.session_state.movs = pd.DataFrame(columns=['Tipo', 'Produto', 'Qtd', 'Motivo', 'Data'])

df = st.session_state.estoque
df['Status_Critico'] = (df['Qtd'] <= (df['Minimo'] * 0.20))
df['Valor_Total'] = df['Qtd'] * df['Preco']

# 4. MENU
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>🏢 Almoxarifado</h2>", unsafe_allow_html=True)
    escolha = option_menu(None, ["Painel", "Produtos", "Movimentações"], 
        icons=["grid-1x2", "box", "arrow-left-right"], default_index=0,
        styles={"container": {"background-color": "#0f172a"}, "nav-link": {"color": "#94a3b8", "font-size": "15px"}, "nav-link-selected": {"background-color": "#1e293b"}})

# 5. PÁGINAS
if escolha == "Painel":
    st.title("📊 Visão Geral")
    c1, c2, c3 = st.columns(3)
    c1.metric("Itens Críticos", len(df[df['Status_Critico']]))
    c2.metric("Patrimônio", f"R$ {df['Valor_Total'].sum():,.2f}")
    c3.metric("Saldo Total", int(df['Qtd'].sum()))
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.pie(df, values='Qtd', names='Categoria', hole=0.6, title="Distribuição")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        criticos = df[df['Status_Critico']]
        if not criticos.empty:
            st.subheader("Estoque Crítico")
            st.bar_chart(criticos.set_index('Produto')['Qtd'])
        else:
            st.success("Estoque OK!")

elif escolha == "Produtos":
    st.title("📦 Inventário")
    with st.expander("➕ Novo Produto"):
        with st.form("n_prod"):
            n_p = st.text_input("Nome")
            n_c = st.selectbox("Cat", ["Elétrica", "Hidráulica", "Fixação"])
            n_m = st.number_input("Mínimo", min_value=1)
            n_v = st.number_input("Preço", min_value=0.0)
            if st.form_submit_button("Salvar"):
                novo = pd.DataFrame([{'Produto': n_p, 'Categoria': n_c, 'Qtd': 0, 'Minimo': n_m, 'Preco': n_v}])
                st.session_state.estoque = pd.concat
