import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from io import BytesIO
import base64
import os
import scipy.stats as stats
from adjustText import adjust_text
import subprocess

# Configuração da página inicial
st.set_page_config(page_title="Gerador de Relatórios Ambientais", layout="wide")

# CSS para melhoria da interface
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        padding: 20px;
    }
    .block-container {
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTitle {
        color: #2E4053;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    .stHeader {
        color: #4CAF50;
        font-size: 24px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Página inicial
if "inicio" not in st.session_state:
    st.session_state.inicio = False

if not st.session_state.inicio:
    st.markdown("<h1 class='stTitle'>🌿 Gerador de Relatórios Ambientais</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='stHeader'>Automatize a criação de relatórios ambientais com análises fitossociológicas e estruturais.</h2>", unsafe_allow_html=True)
    if st.button("🚀 Iniciar Elaboração"):
        st.session_state.inicio = True
        st.rerun()
else:
    # Criando um fluxo passo a passo
    st.markdown("<h2 class='stHeader'>📌 Tipo de Inventário</h2>", unsafe_allow_html=True)
    tipo_inventario = st.selectbox("Selecione o tipo de inventário:", ["Amostragem por parcelas", "Censo florestal"])
    
    if "tipo_inventario" not in st.session_state:
        st.session_state.tipo_inventario = tipo_inventario
    
    if tipo_inventario == "Amostragem por parcelas":
        st.markdown("<h2 class='stHeader'>🔍 Tipo de Análise</h2>", unsafe_allow_html=True)
        tipo_analise = st.selectbox("Escolha o tipo de análise:", ["Casual Simples", "Estratificada"])

        tamanho_parcela = st.number_input("📏 Tamanho da parcela (m²)", min_value=1, value=100)
        area_inventario = st.number_input("🌍 Tamanho da área do inventário (ha)", min_value=0.1, value=1.0)
        
        if tipo_analise == "Estratificada":
            num_estratos = st.number_input("📊 Número de Estratos", min_value=1, value=2, step=1)
            estratos = []
            for i in range(int(num_estratos)):
                with st.expander(f"🔹 Configuração do Estrato {i+1}"):
                    nome_estrato = st.text_input(f"📛 Nome do Estrato {i+1}")
                    area_estrato = st.number_input(f"📏 Área do Estrato {i+1} (ha)", min_value=0.1, value=1.0)
                    num_parcelas = st.number_input(f"📌 Número de Parcelas no Estrato {i+1}", min_value=1, value=5, step=1)
                    estratos.append(f"{nome_estrato}:{area_estrato}:{num_parcelas}")
            estratos_info = "|".join(estratos)
    else:
        tamanho_parcela = None
        area_inventario = st.number_input("🌍 Tamanho da área do inventário (ha)", min_value=0.1, value=1.0)
    
    st.markdown("<h2 class='stHeader'>📂 Enviar Arquivo de Dados</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Faça upload do arquivo Excel contendo os dados do inventário florestal", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.markdown("### 🔍 Prévia dos Dados")
        st.dataframe(df.head())

        if st.button("📊 Gerar Relatório"):
            abundancias = ','.join(map(str, df.groupby('Espécie')['Diâmetro (cm)'].sum().tolist()))
            
            resultados_r = subprocess.run(
                ["Rscript", "analises_florestais.R", abundancias, "dados_inventario.xlsx", "30", str(area_inventario), tipo_inventario, "N/A", str(tamanho_parcela), str(area_inventario)],
                capture_output=True,
                text=True
            ).stdout
            
            st.markdown("### 📑 Resultados das Análises Estatísticas (R)")
            st.text(resultados_r)
