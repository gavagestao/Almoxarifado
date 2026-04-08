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

# PROTEÇÃO CONTRA ERROS DE TIPO (FORÇAR NÚMEROS)
df = st.session_state.estoque.copy()
df['Qtd'] = pd.to_numeric(df['Qtd'], errors='coerce').fillna(0)
df['Minimo'] = pd.to_numeric(df['Minimo'], errors='coerce').fillna(1)
df['Preco'] = pd.to_numeric(df['Preco'], errors='coerce').fillna(0)

# CÁLCULOS
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
        if not df.empty:
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
            n_c = st.selectbox("Cat", ["Elétrica", "Hidráulica", "Fixação", "Outros"])
            n_m = st.number_input("Mínimo (Meta 100%)", min_value=1, value=100)
            n_v = st.number_input("Preço Unitário", min_value=0.0, value=1.0)
            if st.form_submit_button("Salvar"):
                novo = pd.DataFrame([{'Produto': n_p, 'Categoria': n_c, 'Qtd': 0, 'Minimo': n_m, 'Preco': n_v}])
                st.session_state.estoque = pd.concat([st.session_state.estoque, novo], ignore_index=True)
                st.rerun()
    st.dataframe(st.session_state.estoque, use_container_width=True)

elif escolha == "Movimentações":
    st.title("🔄 Entradas e Saídas")
    with st.expander("🚀 Registrar"):
        with st.form("n_mov"):
            m_p = st.selectbox("Produto", df['Produto'].unique())
            m_t = st.radio("Tipo", ["Entrada", "Saída"], horizontal=True)
            m_q = st.number_input("Qtd", min_value=1, value=1)
            m_m = st.text_input("Motivo")
            if st.form_submit_button("Confirmar"):
                idx = st.session_state.estoque[st.session_state.estoque['Produto'] == m_p].index[0]
                if m_t == "Entrada": 
                    st.session_state.estoque.at[idx, 'Qtd'] += m_q
                else: 
                    st.session_state.estoque.at[idx, 'Qtd'] -= m_q
                
                nova = pd.DataFrame([{'Tipo': m_t, 'Produto': m_p, 'Qtd': m_q, 'Motivo': m_m, 'Data': datetime.now().strftime("%d/%m/%Y")}])
                st.session_state.movs = pd.concat([nova, st.session_state.movs], ignore_index=True)
                st.rerun()
    
    for _, r in st.session_state.movs.iterrows():
        c1, c2, c3, c4 = st.columns([1, 3, 1, 3])
        s = "badge-entrada" if r['Tipo'] == "Entrada" else "badge-saida"
        c1.markdown(f'<span class="{s}">{r["Tipo"]}</span>', unsafe_allow_html=True)
        c2.markdown(f"**{r['Produto']}**")
        c3.write(r['Qtd'])
        c4.write(f"{r['Data']} - {r['Motivo']}")
        st.markdown("<hr>", unsafe_allow_html=True)
