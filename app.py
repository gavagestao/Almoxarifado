import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Instaladora Pro", layout="wide")

# 2. ESTILO CSS COMPLETO (Premium + Correção de Cores)
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { color: #1e293b !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    [data-testid="stMetric"] { background-color: white !important; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; }
    .status-normal { background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    .status-regular { background-color: #fef9c3; color: #854d0e; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    .status-alerta { background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    .badge-cat { background-color: #f1f5f9; color: #475569; padding: 2px 10px; border-radius: 10px; font-size: 12px; }
    .badge-entrada { background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 8px; font-weight: bold; }
    .badge-saida { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 8px; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #0f172a; }
    hr { margin: 8px 0 !important; border-top: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# 3. GERENCIAMENTO DE DADOS
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'Nome': 'Parafuso Phillips 6mm', 'Categoria': 'Fixação', 'Qtd': 450, 'Unidade': 'un', 'Meta': 1000},
        {'Nome': 'Fita Isolante Preta', 'Categoria': 'Elétrica', 'Qtd': 25, 'Unidade': 'rolo', 'Meta': 100},
        {'Nome': 'Luva de Procedimento M', 'Categoria': 'EPI', 'Qtd': 8, 'Unidade': 'cx', 'Meta': 50}
    ])

if 'movs' not in st.session_state:
    st.session_state.movs = pd.DataFrame([
        {'Tipo': 'Entrada', 'Produto': 'Parafuso Phillips 6mm', 'Qtd': 200, 'Motivo': 'Compra fornecedor', 'Data': '31/10/2024'},
        {'Tipo': 'Saída', 'Produto': 'Luva de Procedimento M', 'Qtd': 5, 'Motivo': 'Uso setor produção', 'Data': '04/11/2024'}
    ])

def get_status(q, m):
    p = (q / m) * 100 if m > 0 else 0
    if p >= 40: return "Normal", "status-normal"
    if p >= 21: return "Regular", "status-regular"
    return "Abaixo", "status-alerta"

# 4. MENU LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:white;text-align:center;'>🏢 Sistema</h2>", unsafe_allow_html=True)
    menu = option_menu(None, ["Painel", "Produtos", "Movimentações"], 
        icons=["grid", "box", "arrow-repeat"], default_index=0)

# 5. PÁGINAS
if menu == "Painel":
    st.title("📊 Visão Geral da Obra")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    criticos = sum(1 for i, r in st.session_state.estoque.iterrows() if (r['Qtd']/r['Meta']) <= 0.2)
    c1.metric("Itens Críticos", criticos)
    c2.metric("Patrimônio Est.", f"R$ {st.session_state.estoque['Qtd'].sum() * 5:,.2f}")
    c3.metric("Saldo Total", int(st.session_state.estoque['Qtd'].sum()))
    c4.metric("Obras Ativas", "2")
    
    st.markdown("---")
    
    # Gráficos
    g1, g2 = st.columns(2)
    with g1:
        fig_pie = px.pie(st.session_state.estoque, values='Qtd', names='Categoria', hole=0.5, title="Distribuição por Categoria")
        st.plotly_chart(fig_pie, use_container_width=True)
    with g2:
        fig_bar = px.bar(st.session_state.estoque, x='Nome', y='Qtd', color='Categoria', title="Saldo por Produto")
        st.plotly_chart(fig_bar, use_container_width=True)

elif menu == "Produtos":
    st.title("📦 Inventário de Produtos")
    
    with st.expander("➕ Cadastrar Novo Material"):
        with st.form("novo_p"):
            f1, f2 = st.columns(2)
            n = f1.text_input("Nome do Material")
            c = f2.selectbox("Categoria", ["Fixação", "Elétrica", "EPI", "Hidráulica"])
            f3, f4 = st.columns(2)
            u = f3.text_input("Unidade (un, rolo, m)")
            m = f4.number_input("Meta de Estoque (100%)", min_value=1)
            if st.form_submit_button("Salvar"):
                novo = pd.DataFrame([{'Nome': n, 'Categoria': c, 'Qtd': 0, 'Unidade': u, 'Meta': m}])
                st.session_state.estoque = pd.concat([st.session_state.estoque, novo], ignore_index=True)
                st.rerun()

    busca = st.text_input("🔍 Buscar material...", placeholder="Ex: Parafuso")
    st.markdown("---")
    
    # Tabela Premium
    h = st.columns([4, 2, 1, 1, 2, 0.5])
    for col, txt in zip(h, ["Nome", "Categoria", "Qtd.", "Un.", "Status", ""]): col.caption(txt)

    for i, r in st.session_state.estoque.iterrows():
        if busca.lower() in r['Nome'].lower() or busca.lower() in r['Categoria'].lower():
            cols = st.columns([4, 2, 1, 1, 2, 0.5])
            cols[0].write(f"**{r['Nome']}**")
            cols[1].markdown(f'<span class="badge-cat">{r["Categoria"]}</span>', unsafe_allow_html=True)
            cols[2].write(str(int(r['Qtd'])))
            cols[3].write(r['Unidade'])
            txt, cl = get_status(r['Qtd'], r['Meta'])
            cols[4].markdown(f'<span class="{cl}">{txt}</span>', unsafe_allow_html=True)
            if cols[5].button("🗑️", key=f"del_{i}"):
                st.session_state.estoque = st.session_state.estoque.drop(i).reset_index(drop=True)
                st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

elif menu == "Movimentações":
    st.title("🔄 Registro de Entradas e Saídas")
    
    with st.expander("🚀 Lançar Movimentação"):
        with st.form("mov"):
            p_sel = st.selectbox("Selecione o Produto", st.session_state.estoque['Nome'].unique())
            t_mov = st.radio("Tipo", ["Entrada", "Saída"], horizontal=True)
            q_mov = st.number_input("Quantidade", min_value=1)
            m_mov = st.text_input("Motivo/Destino")
            if st.form_submit_button("Confirmar"):
                idx = st.session_state.estoque[st.session_state.estoque['Nome'] == p_sel].index[0]
                if t_mov == "Entrada": st.session_state.estoque.at[idx, 'Qtd'] += q_mov
                else: st.session_state.estoque.at[idx, 'Qtd'] -= q_mov
                
                nova_mov = pd.DataFrame([{'Tipo': t_mov, 'Produto': p_sel, 'Qtd': q_mov, 'Motivo': m_mov, 'Data': datetime.now().strftime("%d/%m/%Y")}])
                st.session_state.movs = pd.concat([nova_mov, st.session_state.movs], ignore_index=True)
                st.rerun()

    # Tabela de Histórico
    st.markdown("---")
    for _, r in st.session_state.movs.iterrows():
        c1, c2, c3, c4 = st.columns([1, 3, 1, 3])
        bad = "badge-entrada" if r['Tipo'] == "Entrada" else "badge-saida"
        c1.markdown(f'<span class="{bad}">{r["Tipo"]}</span>', unsafe_allow_html=True)
        c2.write(f"**{r['Produto']}**")
        c3.write(f"{r['Qtd']}")
        c4.caption(f"{r['Data']} - {r['Motivo']}")
        st.markdown("<hr>", unsafe_allow_html=True)
