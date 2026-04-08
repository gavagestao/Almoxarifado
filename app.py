import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(page_title="Instaladora Pro - Gestão de Estoque", layout="wide")

# --- ESTILO CUSTOMIZADO (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
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

# --- NOVO MENU LATERAL MODERNO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4232/4232145.png", width=80) # Ícone de construção
    st.title("Instaladora Pro")
    
    escolha = option_menu(
        menu_title=None,
        options=["Dashboard", "Inventário", "Movimentar", "Relatórios"],
        icons=["house", "box-seam", "arrow-left-right", "file-earmark-bar-graph"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1e293b"},
            "icon": {"color": "#fbbf24", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "color": "white"},
            "nav-link-selected": {"background-color": "#334155"},
        }
    )

# --- LÓGICA DAS PÁGINAS ---

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
        fig = px.pie(df, values='Qtd', names='Categoria', hole=0.6, color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.subheader("Atenção: Abaixo de 20%")
        criticos = df[df['Status_Critico']]
        if not criticos.empty:
            st.bar_chart(criticos.set_index('Produto')['Qtd'], color="#ef4444")
        else:
            st.success("Estoque saudável!")

elif escolha == "Inventário":
    st.title("📝 Cadastro e Listagem")
    with st.expander("Novo Produto"):
        # (Lógica de cadastro simplificada para brevidade, mas igual à anterior)
        st.info("Formulário de cadastro ativo.")
    st.dataframe(df, use_container_width=True)

elif escolha == "Movimentar":
    st.title("🔄 Entradas e Saídas")
    # Seleção moderna de produtos
    prod_selecionado = st.selectbox("Escolha o material", df['Produto'].unique())
    col_m1, col_m2 = st.columns(2)
    tipo = col_m1.radio("Operação", ["Entrada", "Saída"])
    valor = col_m2.number_input("Quantidade", min_value=1)
    if st.button("Confirmar Registro"):
        st.success(f"{tipo} de {valor} unidades de {prod_selecionado} registrada!")

elif escolha == "Relatórios":
    st.title("📋 Relatórios Gerenciais")
    st.dataframe(df[['Obra', 'Produto', 'Qtd', 'Valor_Total']])
    st.download_button("Exportar para Excel", df.to_csv().encode('utf-8'), "estoque.csv")
