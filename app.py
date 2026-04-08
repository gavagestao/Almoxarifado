import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Gestão de Estoque - Instaladora", layout="wide")

# Simulação de Banco de Dados (Em um sistema real, usaríamos SQL)
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {'ID': 1, 'Produto': 'Cabo Flexível 2.5mm', 'Categoria': 'Elétrica', 'Qtd': 100, 'Minimo': 500},
        {'ID': 2, 'Produto': 'Tubo PVC 100mm', 'Categoria': 'Hidráulica', 'Qtd': 15, 'Minimo': 100},
        {'ID': 3, 'Produto': 'Disjuntor DIN 20A', 'Categoria': 'Elétrica', 'Qtd': 50, 'Minimo': 60},
    ])

# --- CÁLCULOS DE DASHBOARD ---
df = st.session_state.estoque
df['Status_Critico'] = (df['Qtd'] <= (df['Minimo'] * 0.20))

# --- MENU LATERAL ---
menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Estoque & Cadastro", "Movimentações", "Relatórios Diretores"])

# --- 1. DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Painel de Controle de Obras")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Itens Críticos (<20%)", len(df[df['Status_Critico']]))
    col2.metric("Total de Itens", df['Qtd'].sum())
    col3.metric("Categorias Ativas", df['Categoria'].nunique())

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📦 Quantidade por Categoria")
        fig_cat = px.pie(df, values='Qtd', names='Categoria', hole=0.4)
        st.plotly_chart(fig_cat)
        
    with c2:
        st.subheader("⚠️ Estado Crítico (Abaixo de 20% do Ideal)")
        criticos = df[df['Status_Critico']]
        if not criticos.empty:
            fig_critico = px.bar(criticos, x='Produto', y='Qtd', color_discrete_sequence=['red'])
            st.plotly_chart(fig_critico)
        else:
            st.success("Nenhum item em estado crítico!")

# --- 2. ESTOQUE & CADASTRO ---
elif menu == "Estoque & Cadastro":
    st.title("📝 Cadastro e Inventário")
    
    with st.expander("Cadastrar Novo Produto"):
        novo_p = st.text_input("Nome do Produto")
        nova_cat = st.selectbox("Categoria", ["Elétrica", "Hidráulica", "Infraestrutura", "Civil"])
        minimo = st.number_input("Estoque Ideal (100%)", min_value=1)
        if st.button("Salvar"):
            st.success(f"{novo_p} cadastrado com sucesso!")

    st.subheader("Lista de Materiais")
    st.dataframe(df, use_container_width=True)

# --- 3. MOVIMENTAÇÕES ---
elif menu == "Movimentações":
    st.title("🔄 Entradas, Saídas e Transferências")
    
    tipo = st.radio("Tipo de Operação", ["Entrada", "Saída", "Transferência Recebida", "Transferência Enviada"])
    prod = st.selectbox("Selecione o Produto", df['Produto'].tolist())
    qtd_mov = st.number_input("Quantidade", min_value=1)
    
    if st.button("Confirmar Movimentação"):
        st.warning(f"Movimentação de {qtd_mov} unidades de {prod} registrada no histórico.")

# --- 4. RELATÓRIOS ---
elif menu == "Relatórios Diretores":
    st.title("📋 Relatórios Executivos")
    st.write("Dados consolidados para exportação.")
    
    st.table(df[['Produto', 'Categoria', 'Qtd', 'Minimo']])
    
    st.download_button(
        label="📥 Baixar Relatório Completo (CSV)",
        data=df.to_csv().encode('utf-8'),
        file_name='relatorio_estoque_obra.csv',
        mime='text/csv',
    )
