import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="🚛 Controle de Pátio",
    page_icon="🚛",
    layout="wide"
)

# ============================================
# URL DA SUA PLANILHA (JÁ CONFIGURADA)
# ============================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqJKCZimAb2vkXJZpSezpLza2q-fgdSqoKlxGYsTQzURfSu5aLIGXAHuBK_xKL9XBsQcEeyOqLcRWA/pub?output=csv"

# ============================================
# ESTILO PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stMetric > div {
        font-size: 1.2rem !important;
    }
    .stMetric > div:nth-child(2) {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .dataframe {
        font-size: 1.1rem !important;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e63939;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CARREGAR DADOS DA PLANILHA
# ============================================
@st.cache_data(ttl=15)
def carregar_dados():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar dados: {e}")
        return pd.DataFrame()

# ============================================
# CABEÇALHO
# ============================================
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.markdown("## 🚛")
with col_titulo:
    st.title("Controle de Pátio - Tempo Real")

st.markdown("### Atualização automática a cada 15 segundos • Nenhum toque necessário")

# ============================================
# DADOS
# ============================================
df = carregar_dados()

if len(df) > 0 and 'Status' in df.columns:
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Contar veículos no pátio (busca parcial para evitar erros de formatação)
    no_patio = len(df[df['Status'].astype(str).str.contains('No Pátio', na=False)])
    
    # Tentar detectar data de hoje em diferentes formatos
    hoje_str = datetime.now().strftime('%d/%m/%Y')
    entradas_hoje = len(df[df['Data'].astype(str).str.contains(hoje_str, na=False)])
    
    saidas_hoje = len(df[
        (df['Data'].astype(str).str.contains(hoje_str, na=False)) & 
        (df['Status'].astype(str).str.contains('Saída', na=False))
    ])
    
    with col1:
        st.metric("🚛 No Pátio", no_patio)
    with col2:
        st.metric("✅ Entradas Hoje", entradas_hoje)
    with col3:
        st.metric("🚪 Saídas Hoje", saidas_hoje)
    with col4:
        st.metric("📊 Total Registros", len(df))
    
    st.markdown("---")
    
    # Veículos no pátio
    st.subheader("🚛 Veículos Atualmente no Pátio")
    df_patio = df[df['Status'].astype(str).str.contains('No Pátio', na=False)]
    
    if len(df_patio) > 0:
        cols_patio = ['Placa', 'Tipo', 'Motorista', 'Empresa', 'Entrada']
        cols_patio = [c for c in cols_patio if c in df_patio.columns]
        
        st.dataframe(
            df_patio[cols_patio],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("📭 Pátio vazio no momento")
    
    st.markdown("---")
    
    # Últimas movimentações
    st.subheader("📋 Últimas 10 Movimentações")
    df_ultimas = df.tail(10)
    cols_ultimas = ['Data', 'Entrada', 'Placa', 'Tipo', 'Status']
    cols_ultimas = [c for c in cols_ultimas if c in df_ultimas.columns]
    
    st.dataframe(
        df_ultimas[cols_ultimas],
        use_container_width=True,
        hide_index=True
    )
    
else:
    st.warning("""
    📌 **Planilha vazia ou sem colunas necessárias**
    
    Para começar:
    1. Abra sua planilha: https://docs.google.com/spreadsheets/d/1vTqJKCZimAb2vkXJZpSezpLza2q-fgdSqoKlxGYsTQzURfSu5aLIGXAHuBK_xKL9XBsQcEeyOqLcRWA/edit
    2. Certifique-se de ter estas colunas na linha 1:
       - A1: Data | B1: Entrada | C1: Placa | D1: Tipo | E1: Motorista | F1: Empresa | G1: Saída | H1: Status
    3. Adicione pelo menos 1 registro
    4. O dashboard atualizará automaticamente em 15 segundos
    """)

# Auto-refresh a cada 15 segundos
st.markdown(
    """
    <meta http-equiv="refresh" content="15">
    """,
    unsafe_allow_html=True
)

# Rodapé
st.markdown("---")
st.caption("✅ Atualização automática • 📱 Acesso mobile • 🚀 Zero configuração para diretores")