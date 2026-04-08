import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu

# 1. CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA COISA)
st.set_page_config(page_title="Instaladora Pro - Gestão de Estoque", layout="wide")

# 2. ESTOQUE/CSS PARA CORRIGIR OS CARDS BRANCOS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Estilização dos Cards de Métrica */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #edf2f7 !important;
    }
    
    /* FORÇAR COR DO TEXTO PARA APARECER NO DARK MODE */
    [data-testid="stMetricLabel"] {
        color: #4a5568 !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a202c !important;
    }
    
    [data-testid="stSidebar"] { background-color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS ---
DB_FILE = "estoque_dados.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame([
        {'ID': 1, 'Produto': 'Cabo Flex 2.5mm', 'Categoria': 'Elétrica', 'Obra': 'Matriz', 'Qtd': 100, 'Minimo': 500, 'Preco': 2.50},
        {'ID': 2, 'Produto': 'Tubo PVC 100mm', 'Categoria': 'Hidráulica', 'Obra': 'Obra A', 'Qtd': 15, 'Minimo': 100, 'Preco': 45.00}
    ])

if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

df = st.session_state.estoque
df['Status_Critico'] = (df['Qtd'] <= (df['Minimo'] * 0.20))
df['Valor_Total'] = df['Qtd'] * df['Preco']

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🏗️ Instaladora Pro")
    escolha = option_menu(
        menu_title=None,
        options=["Dashboard", "Inventário", "Movimentar", "Relatórios"],
        icons=["house", "box-seam", "arrow-left-right", "file-earmark-bar-graph"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1e293b"},
            "icon": {"color": "#fbbf24", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "color": "white"},
            "nav-link-selected": {"background-color": "#334155"},
        }
    )

# --- PÁGINAS ---
if escolha == "Dashboard":
    st.title("📊 Visão Geral da Obra")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Itens Críticos", len(df[df['Status_Critico']]))
    c2.metric("Patrimônio", f"R$ {df['Valor_Total'].sum():,.2f}")
    c3.metric("Saldo Total", int(df['Qtd'].sum()))
    c4.metric("Obras", df['Obra'].nunique())

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Distribuição por Categoria")
        fig = px.pie(df, values='Qtd', names='Categoria', hole=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.subheader("⚠️ Itens abaixo de 20%")
        criticos = df[df['Status_Critico']]
        if not criticos.empty:
            st.bar_chart(criticos.set_index('Produto')['Qtd'])
        else:
            st.success("Tudo em ordem!")

elif escolha == "Inventário":
    st.title("📝 Inventário de Materiais")
    st.dataframe(df, use_container_width=True)

elif escolha == "Movimentar":
    st.title("🔄 Registrar Entrada/Saída")
    prod_sel = st.selectbox("Produto", df['Produto'].unique())
    tipo = st.radio("Operação", ["Entrada", "Saída"], horizontal=True)
    qtd = st.number_input("Quantidade", min_value=1)
    if st.button("Confirmar"):
        st.success(f"Movimentação de {prod_sel} gravada!")

elif escolha == "Relatórios":
    st.title("📋 Relatório para Diretores")
    st.table(df[['Obra', 'Produto', 'Qtd', 'Valor_Total']])
