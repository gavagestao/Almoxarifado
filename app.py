import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Instaladora Pro", layout="wide")

# 2. ESTILO CSS (Visual Premium e Badges)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* Badges de Status */
    .status-normal { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #bbf7d0; }
    .status-regular { background-color: #fef9c3; color: #854d0e; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #fef08a; }
    .status-alerta { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #fecaca; }
    
    /* Badges de Categoria */
    .badge-cat { background-color: #e2e8f0; color: #475569; padding: 2px 10px; border-radius: 10px; font-size: 12px; }
    
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 8px 0 !important; border-top: 1px solid #e2e8f0 !important; }
    
    /* Botão de excluir */
    .stButton>button { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANCO DE DADOS ---
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Nome': 'Parafuso Phillips 6mm', 'Categoria': 'Fixação', 'Qtd': 450, 'Unidade': 'un', 'Meta': 1000},
        {'Nome': 'Fita Isolante Preta', 'Categoria': 'Elétrica', 'Qtd': 25, 'Unidade': 'rolo', 'Meta': 100},
        {'Nome': 'Luva de Procedimento M', 'Categoria': 'EPI', 'Qtd': 8, 'Unidade': 'cx', 'Meta': 50}
    ])

# Função corrigida para o Status
def calcular_status(qtd, meta):
    if meta <= 0: return "Abaixo", "status-alerta"
    percentual = (qtd / meta) * 100
    if percentual >= 40: return "Normal", "status-normal"
    elif 21 <= percentual <= 39: return "Regular", "status-regular"
    else: return "Abaixo", "status-alerta"

# --- 4. MENU LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:white; text-align:center;'>🏢 Almoxarifado</h2>", unsafe_allow_html=True)
    escolha = option_menu(None, ["Painel", "Produtos", "Movimentações"], 
        icons=["grid-1x2", "box", "arrow-left-right"], default_index=1)

# --- 5. PÁGINA PRODUTOS ---
if escolha == "Produtos":
    col_h1, col_h2 = st.columns([8, 2])
    col_h1.title("Produtos")
    
    # Modal de Cadastro (Expander)
    with st.expander("➕ Novo Produto"):
        with st.form("cad_prod"):
            f_nome = st.text_input("Nome do Material")
            f_cat = st.selectbox("Categoria", ["Fixação", "Elétrica", "EPI", "Hidráulica", "Outros"])
            f_un = st.text_input("Unidade (ex: un, rolo, cx)")
            f_meta = st.number_input("Estoque Ideal (Meta 100%)", min_value=1)
            if st.form_submit_button("Salvar Produto"):
                novo = pd.DataFrame([{'Nome': f_nome, 'Categoria': f_cat, 'Qtd': 0, 'Unidade': f_un, 'Meta': f_meta}])
                st.session_state.estoque = pd.concat([st.session_state.estoque, novo], ignore
