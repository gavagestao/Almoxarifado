import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO E ESTILO (CORRIGE TEXTO INVISÍVEL)
st.set_page_config(page_title="Instaladora Pro", layout="wide")
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { color: #1e293b !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    [data-testid="stMetric"] { background-color: white !important; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; }
    .status-normal { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .status-regular { background-color: #fef9c3; color: #854d0e; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .status-alerta { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .badge-cat { background-color: #f1f5f9; color: #475569; padding: 2px 10px; border-radius: 10px; font-size: 12px; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 8px 0 !important; border-top: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# 2. BANCO DE DADOS INICIAL
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Nome': 'Parafuso Phillips 6mm', 'Categoria': 'Fixação', 'Qtd': 450, 'Unidade': 'un', 'Meta': 1000},
        {'Nome': 'Fita Isolante Preta', 'Categoria': 'Elétrica', 'Qtd': 25, 'Unidade': 'rolo', 'Meta': 100},
        {'Nome': 'Luva de Procedimento M', 'Categoria': 'EPI', 'Qtd': 8, 'Unidade': 'cx', 'Meta': 50}
    ])

def get_status(q, m):
    p = (q / m) * 100 if m > 0 else 0
    if p >= 40: return "Normal", "status-normal"
    if p >= 21: return "Regular", "status-regular"
    return "Abaixo", "status-alerta"

# 3. MENU LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:white;text-align:center;'>🏢 Sistema</h2>", unsafe_allow_html=True)
    menu = option_menu(None, ["Painel", "Produtos", "Movimentações"], icons=["grid", "box", "arrow-repeat"], default_index=0)

# 4. PÁGINAS
if menu == "Painel":
    st.title("📊 Visão Geral da Obra")
    c1, c2, c3, c4 = st.columns(4)
    # Regras de cálculo baseadas na Meta
    criticos = sum(1 for i, r in st.session_state.estoque.iterrows() if (r['Qtd']/r['Meta']) <= 0.2)
    c1.metric("Itens Críticos", criticos)
    c2.metric("Patrimônio Est.", "R$ 1.250,00")
    c3.metric("Saldo Total", int(st.session_state.estoque['Qtd'].sum()))
    c4.metric("Obras Ativas", "2")

elif menu == "Produtos":
    st.title("Produtos")
    busca = st.text_input("🔍 Buscar...", placeholder="Nome ou categoria")
    st.markdown("---")
    h = st.columns([4, 2, 1, 1, 2, 0.5])
    for col, txt in zip(h, ["Nome", "Categoria", "Qtd.", "Un.", "Status", ""]): col.caption(txt)

    for i, r in st.session_state.estoque.iterrows():
        if busca.lower() in r['Nome'].lower() or busca.lower() in r['Categoria'].lower():
            c = st.columns([4, 2, 1, 1, 2, 0.5])
            c[0].write(f"**{r['Nome']}**")
            c[1].markdown(f'<span class="badge-cat">{r["Categoria"]}</span>', unsafe_allow_html=True)
            c[2].write(str(int(r['Qtd'])))
            c[3].write(r['Unidade'])
            txt, cl = get_status(r['Qtd'], r['Meta'])
            c[4].markdown(f'<span class="{cl}">{txt}</span>', unsafe_allow_html=True)
            if c[5].button("🗑️", key=f"d{i}"):
                st.session_state.estoque = st.session_state.estoque.drop(i).reset_index(drop=True)
                st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

else:
    st.title("🔄 Movimentações")
    st.info("Página de histórico configurada.")
