import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página
st.set_page_config(page_title="Sistema de Estoque - Instaladora", layout="wide")

# --- FUNÇÕES DE BANCO DE DADOS (CSV) ---
DB_FILE = "estoque_dados.csv"

def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        # Dados iniciais caso o arquivo não exista
        return pd.DataFrame([
            {'ID': 1, 'Produto': 'Cabo Flex 2.5mm', 'Categoria': 'Elétrica', 'Obra': 'Matriz', 'Qtd': 100, 'Minimo': 500, 'Preco': 2.50},
            {'ID': 2, 'Produto': 'Tubo PVC 100mm', 'Categoria': 'Hidráulica', 'Obra': 'Obra Residencial A', 'Qtd': 15, 'Minimo': 100, 'Preco': 45.00}
        ])

def salvar_dados(df):
    df.to_csv(DB_FILE, index=False)

# Inicializar dados na sessão
if 'estoque' not in st.session_state:
    st.session_state.estoque = carregar_dados()

df = st.session_state.estoque

# --- CÁLCULOS TÉCNICOS ---
df['Status_Critico'] = (df['Qtd'] <= (df['Minimo'] * 0.20))
df['Valor_Total'] = df['Qtd'] * df['Preco']

# --- INTERFACE LATERAL ---
st.sidebar.title("🛠️ Gestão de Instaladora")
menu = st.sidebar.radio("Selecione a Área", ["Painel Geral", "Inventário", "Entradas/Saídas", "Relatório Executivo"])

# --- 1. PAINEL GERAL (DASHBOARD) ---
if menu == "Painel Geral":
    st.title("📊 Dashboard de Materiais")
    
    # Métricas principais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Itens Críticos (<20%)", len(df[df['Status_Critico']]), delta_color="inverse")
    c2.metric("Patrimônio em Estoque", f"R$ {df['Valor_Total'].sum():,.2f}")
    c3.metric("Total de Unidades", int(df['Qtd'].sum()))
    c4.metric("Obras Ativas", df['Obra'].nunique())

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📦 Volume por Categoria")
        fig_pie = px.pie(df, values='Qtd', names='Categoria', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("⚠️ Alerta: Estoque Crítico (Abaixo de 20%)")
        criticos = df[df['Status_Critico']].copy()
        if not criticos.empty:
            fig_bar = px.bar(criticos, x='Produto', y='Qtd', color='Obra', title="Produtos para Reposição Imediata")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.success("Tudo em ordem! Nenhum item abaixo do nível de segurança.")

# --- 2. INVENTÁRIO & CADASTRO ---
elif menu == "Inventário":
    st.title("📝 Cadastro de Materiais")
    
    with st.expander("➕ Adicionar Novo Item ao Estoque"):
        with st.form("form_cadastro"):
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome do Produto (especificações)")
            cat = c2.selectbox("Categoria", ["Elétrica", "Hidráulica", "Infraestrutura", "Incêndio", "Ferramentas"])
            c3, c4, c5 = st.columns(3)
            obra_alvo = c3.text_input("Obra/Localização", value="Almoxarifado")
            estoque_ideal = c4.number_input("Estoque 100% (Meta)", min_value=1)
            preco_un = c5.number_input("Preço Unitário (R$)", min_value=0.0, format="%.2f")
            
            if st.form_submit_button("Cadastrar"):
                novo_id = df['ID'].max() + 1 if not df.empty else 1
                novo_item = {
                    'ID': novo_id, 'Produto': nome, 'Categoria': cat, 
                    'Obra': obra_alvo, 'Qtd': 0, 'Minimo': estoque_ideal, 'Preco': preco_un
                }
                st.session_state.estoque = pd.concat([df, pd.DataFrame([novo_item])], ignore_index=True)
                salvar_dados(st.session_state.estoque)
                st.success("Produto cadastrado! Use 'Entradas' para adicionar saldo.")
                st.rerun()

    st.subheader("Tabela Geral de Saldo")
    st.dataframe(df[['ID', 'Produto', 'Categoria', 'Obra', 'Qtd', 'Minimo', 'Preco']], use_container_width=True)

# --- 3. MOVIMENTAÇÕES ---
elif menu == "Entradas/Saídas":
    st.title("🔄 Movimentação de Canteiro")
    
    with st.form("movimentar"):
        produto_sel = st.selectbox("Selecione o Material", df['Produto'].tolist())
        tipo_mov = st.radio("Tipo", ["Entrada (Compra/Sobra)", "Saída (Uso na Obra)", "Transferência"], horizontal=True)
        quantidade = st.number_input("Quantidade da Operação", min_value=1)
        
        if st.form_submit_button("Confirmar Movimentação"):
            idx = df[df['Produto'] == produto_sel].index[0]
            if "Entrada" in tipo_mov:
                df.at[idx, 'Qtd'] += quantidade
            elif "Saída" in tipo_mov:
                if df.at[idx, 'Qtd'] >= quantidade:
                    df.at[idx, 'Qtd'] -= quantidade
                else:
                    st.error("Saldo insuficiente para essa saída!")
                    st.stop()
            
            salvar_dados(df)
            st.success(f"Movimentação de {quantidade} unidades realizada com sucesso!")
            st.rerun()

# --- 4. RELATÓRIO DIRETORIA ---
elif menu == "Relatório Executivo":
    st.title("📋 Relatório para Diretores")
    
    st.markdown("""
    Este relatório consolida o valor financeiro imobilizado e os riscos de parada de obra.
    """)
    
    # Tabela formatada para executivos
    relatorio_df = df[['Obra', 'Categoria', 'Produto', 'Qtd', 'Preco', 'Valor_Total']].copy()
    relatorio_df.columns = ['Local', 'Tipo', 'Descrição', 'Qtd em Mãos', 'Preço Unit.', 'Total R$']
    
    st.table(relatorio_df)
    
    csv = relatorio_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Planilha para Reunião", data=csv, file_name="relatorio_estoque.csv", mime="text/csv")
