import streamlit as st

# Definir configurações da página (TEM QUE SER A PRIMEIRA INSTRUÇÃO)
st.set_page_config(page_title="Gerador de Relatórios Ambientais", layout="wide")

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

# Estilização CSS personalizada com fundo de floresta
st.markdown("""
    <style>
    .main {
        background: url('https://source.unsplash.com/1600x900/?forest') no-repeat center center fixed;
        background-size: cover;
    }
    .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.85);
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
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSidebar {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTitle {
        color: #2E4053;
        font-size: 26px;
        font-weight: bold;
    }
    .stHeader {
        color: #4CAF50;
        font-size: 22px;
    }
    </style>
""", unsafe_allow_html=True)

# Criando o cabeçalho com estilo visual melhorado
st.markdown("<h1 class='stTitle'>🌿 Gerador de Relatórios Ambientais</h1>", unsafe_allow_html=True)
st.markdown("**Automatize a criação de relatórios ambientais com análises fitossociológicas e estruturais.**")

# Criando um layout em colunas
col1, col2 = st.columns([1, 3])

# Criando o formulário de entrada no sidebar
with col1:
    st.sidebar.header("⚙️ Configurações do Inventário")

    tipo_inventario = st.sidebar.selectbox(
        "📌 Tipo de Inventário",
        ["Amostragem por parcelas", "Censo florestal"]
    )

    tipo_analise = None
    estratos_info = ""
    
    if tipo_inventario == "Amostragem por parcelas":
        tipo_analise = st.sidebar.selectbox(
            "🔍 Tipo de Análise",
            ["Casual Simples", "Estratificada"]
        )
        tamanho_parcela = st.sidebar.number_input(
            "📏 Tamanho da parcela (m²)",
            min_value=1, value=100
        )
        area_inventario = st.sidebar.number_input(
            "🌍 Tamanho da área do inventário (ha)",
            min_value=0.1, value=1.0
        )

        if tipo_analise == "Estratificada":
            num_estratos = st.sidebar.number_input("📊 Número de Estratos", min_value=1, value=2, step=1)
            estratos = []
            for i in range(int(num_estratos)):
                with st.sidebar.expander(f"🔹 Configuração do Estrato {i+1}"):
                    nome_estrato = st.text_input(f"📛 Nome do Estrato {i+1}", key=f"nome_{i}")
                    area_estrato = st.number_input(f"📏 Área do Estrato {i+1} (ha)", min_value=0.1, value=1.0, key=f"area_{i}")
                    num_parcelas = st.number_input(f"📌 Número de Parcelas no Estrato {i+1}", min_value=1, value=5, step=1, key=f"parcelas_{i}")
                    estratos.append(f"{nome_estrato}:{area_estrato}:{num_parcelas}")
            estratos_info = "|".join(estratos)
    else:
        tamanho_parcela = None
        area_inventario = st.sidebar.number_input(
            "🌍 Tamanho da área do inventário (ha)",
            min_value=0.1, value=1.0
        )

    # Converter os dados para passar ao script R
    tipo_inventario_r = "amostragem" if tipo_inventario == "Amostragem por parcelas" else "censo"
    tipo_analise_r = tipo_analise if tipo_analise else "N/A"
    tamanho_parcela_r = tamanho_parcela if tamanho_parcela else 0
    tamanho_area_r = area_inventario if area_inventario else 0

# Criando a interface de upload e resultado
with col2:
    st.markdown("<h2 class='stHeader'>📂 Enviar Arquivo de Dados</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Faça upload do arquivo Excel contendo os dados do inventário florestal", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.markdown("### 🔍 Prévia dos Dados")
        st.dataframe(df.head())

        # Botão de geração do relatório com estilo aprimorado
        if st.button("📊 Gerar Relatório"):
            abundancias = ','.join(map(str, df.groupby('Espécie')['Diâmetro (cm)'].sum().tolist()))
            
            # Rodando a análise no R
            resultados_r = subprocess.run(
                ["Rscript", "analises_florestais.R", abundancias, "dados_inventario.xlsx", "30", str(tamanho_area_r), tipo_inventario_r, tipo_analise_r, str(tamanho_parcela_r), str(tamanho_area_r), estratos_info],
                capture_output=True,
                text=True
            ).stdout
            
            # Exibir resultados
            st.markdown("### 📑 Resultados das Análises Estatísticas (R)")
            st.text(resultados_r)
