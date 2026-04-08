import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="PIT 04 - Almoxarifado", layout="wide")

# 2. ESTILO CSS (O segredo para o visual profissional e texto visível)
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { color: #1e293b !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    [data-testid="stMetric"] { background-color: white !important; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px !important; }
    .status-alerta { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .status-normal { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
    .stButton>button:hover { background-color: #e2e8f0; color: #0f172a; }
</style>
""", unsafe_allow_html=True)

# 3. GERENCIAMENTO DE ESTADO (Para os botões funcionarem como links)
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

# 4. BANCO DE DADOS
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Nome': 'Parafuso Phillips 6mm', 'Categoria': 'Fixação', 'Qtd': 450, 'Unidade': 'un', 'Meta': 1000},
        {'Nome': 'Fita Isolante Preta', 'Categoria': 'Elétrica', 'Qtd': 15, 'Unidade': 'rolo', 'Meta': 100},
        {'Nome': 'Luva de Procedimento M', 'Categoria': 'EPI', 'Qtd': 8, 'Unidade': 'cx', 'Meta': 50}
    ])

if 'movs' not in st.session_state:
    ontem = (datetime.now() - timedelta(1)).strftime("%d/%m/%Y")
    st.session_state.movs = pd.DataFrame([
        {'Tipo': 'Entrada', 'Produto': 'Parafuso Phillips 6mm', 'Qtd': 100, 'Data': ontem, 'Motivo': 'Reposição'},
        {'Tipo': 'Saída', 'Produto': 'Fita Isolante Preta', 'Qtd': 5, 'Data': ontem, 'Motivo': 'Uso em Obra'}
    ])

# 5. MENU LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:white;text-align:center;'>🏢 ALMOXARIFADO PIT 04</h2>", unsafe_allow_html=True)
    menu = option_menu(None, ["Painel", "Produtos", "Movimentações"], 
        icons=["grid", "box", "arrow-repeat"], 
        manual_select=st.session_state.page_index,
        key='menu_main')

# 6. PÁGINAS
if menu == "Painel":
    st.title("📊 Painel de Controle")
    
    # Cálculos para os Cards
    ontem_str = (datetime.now() - timedelta(1)).strftime("%d/%m/%Y")
    m_ontem = st.session_state.movs[st.session_state.movs['Data'] == ontem_str]
    
    ent_ontem = m_ontem[m_ontem['Tipo'] == 'Entrada']['Qtd'].sum()
    sai_ontem = m_ontem[m_ontem['Tipo'] == 'Saída']['Qtd'].sum()
    criticos = st.session_state.estoque[st.session_state.estoque['Qtd'] <= (st.session_state.estoque['Meta'] * 0.20)]

    # Layout de Cards Clicáveis
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Entradas (Ontem)", int(ent_ontem))
        if st.button("Ir para Movimentações ➔", key="btn_mov"):
            st.session_state.page_index = 2
            st.rerun()
            
    with c2:
        st.metric("Saídas (Ontem)", int(sai_ontem))
        if st.button("Ver Histórico Completo ➔", key="btn_hist"):
            st.session_state.page_index = 2
            st.rerun()
        
    with c3:
        st.metric("Estoque Crítico", len(criticos))
        if st.button("Ver Itens em Alerta ➔", key="btn_crit"):
            st.session_state.page_index = 1
            st.rerun()

    st.markdown("---")
    fig = px.bar(st.session_state.estoque, x='Nome', y='Qtd', color='Categoria', 
                 title="Saldo Atual de Materiais", color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Produtos":
    st.title("📦 Inventário de Produtos")
    st.info("Dica: Use a busca para encontrar itens com status 'Abaixo'.")
    st.dataframe(st.session_state.estoque, use_container_width=True)

else:
    st.title("🔄 Registro de Movimentações")
    st.write(f"Mostrando dados de: **{ontem_str}**")
    st.table(st.session_state.movs)
