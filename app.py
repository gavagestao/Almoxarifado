# --- ESTILO CUSTOMIZADO (CSS) ---
st.markdown("""
    <style>
    /* Fundo geral da página */
    .main { background-color: #f8f9fa; }
    
    /* Estilização dos Cards de Métrica */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #edf2f7 !important;
    }
    
    /* FORÇAR COR DO TEXTO NAS MÉTRICAS (Para não sumir no Dark Mode) */
    [data-testid="stMetricLabel"] {
        color: #4a5568 !important; /* Cinza escuro para o título */
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a202c !important; /* Preto para o número */
    }
    
    /* Ajuste da barra lateral */
    [data-testid="stSidebar"] { background-color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)
