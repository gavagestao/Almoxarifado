import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(page_title="Instaladora Pro", layout="wide")

# Estilo CSS Consolidado
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .status-normal { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #bbf7d0; }
    .status-regular { background-color: #fef9c3; color: #854d0e; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #fef08a; }
    .status-alerta { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; border: 1px solid #fecaca; }
    .badge-cat { background-color: #e2e8f0; color: #475569; padding: 2px 10px; border-radius: 10px; font-size: 12px; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 8px 0 !important; border-top: 1px solid #e2e8f0 !important; }
    </style>
    """, unsafe_allow_html=True)

# Banco de Dados
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Nome': 'Parafuso Phillips 6mm', 'Categoria': 'Fixação', 'Qtd': 450, 'Unidade': 'un', 'Meta': 1000},
        {'Nome': 'Fita Isolante Preta', 'Categoria': 'Elétrica', 'Qtd': 25, 'Unidade': 'rolo', 'Meta': 100},
        {'Nome': 'Luva de Procedimento M', 'Categoria': 'EPI', 'Qtd': 8, 'Unidade': 'cx', 'Meta': 50}
    ])

if 'movs' not in st.session_state:
    st.session_state.movs = pd
