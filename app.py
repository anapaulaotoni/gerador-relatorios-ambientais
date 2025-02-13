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

def formatar_nome_cientifico(nome):
    """Abrevia a primeira palavra e mantém a segunda para nome científico."""
    palavras = nome.split()
    if len(palavras) >= 2:
        return f"{palavras[0][0]}. {palavras[1]}"
    return nome

def processar_dados(uploaded_file):
    """Processa os dados do arquivo e gera estatísticas."""
    df = pd.read_excel(uploaded_file)
    df = df.rename(columns={"scientific.name": "Espécie", "CAP": "Diâmetro (cm)", "HT": "Altura (m)"})
    
    # Converter colunas para numérico (evitar erro de string)
    df['Diâmetro (cm)'] = pd.to_numeric(df['Diâmetro (cm)'], errors='coerce')
    df['Altura (m)'] = pd.to_numeric(df['Altura (m)'], errors='coerce')
    
    # Remover linhas com valores nulos após conversão
    df = df.dropna(subset=['Diâmetro (cm)', 'Altura (m)'])
    
    df['Volume (m³)'] = np.pi * (df['Diâmetro (cm)'] / 200) ** 2 * df['Altura (m)']
    return df

def rodar_analise_r(abundancias, dados_file, quantidade_de_arvores, area_ua, tipo_inventario, tipo_analise, tamanho_parcela, area_inventario, estratos_info):
    """Executa o script R e captura os resultados."""
    resultado = subprocess.run(
        ["Rscript", "analises_florestais.R", abundancias, dados_file, str(quantidade_de_arvores), str(area_ua), tipo_inventario, tipo_analise, str(tamanho_parcela), str(area_inventario), estratos_info],
        capture_output=True,
        text=True
    )
    return resultado.stdout

# Criando o formulário inicial
st.sidebar.header("Configurações do Inventário")

tipo_inventario = st.sidebar.selectbox(
    "Tipo de Inventário",
    ["Amostragem por parcelas", "Censo florestal"]
)

tipo_analise = None
estratos_info = ""
if tipo_inventario == "Amostragem por parcelas":
    tipo_analise = st.sidebar.selectbox(
        "Tipo de Análise",
        ["Casual Simples", "Estratificada"]
    )
    tamanho_parcela = st.sidebar.number_input(
        "Tamanho da parcela (m²)",
        min_value=1, value=100
    )
    area_inventario = st.sidebar.number_input(
        "Tamanho da área do inventário (ha)",
        min_value=0.1, value=1.0
    )
    
    if tipo_analise == "Estratificada":
        num_estratos = st.sidebar.number_input("Número de Estratos", min_value=1, value=2, step=1)
        estratos = []
        for i in range(int(num_estratos)):
            with st.sidebar.expander(f"Configuração do Estrato {i+1}"):
                nome_estrato = st.text_input(f"Nome do Estrato {i+1}", key=f"nome_{i}")
                area_estrato = st.number_input(f"Área do Estrato {i+1} (ha)", min_value=0.1, value=1.0, key=f"area_{i}")
                num_parcelas = st.number_input(f"Número de Parcelas no Estrato {i+1}", min_value=1, value=5, step=1, key=f"parcelas_{i}")
                estratos.append(f"{nome_estrato}:{area_estrato}:{num_parcelas}")
        estratos_info = "|".join(estratos)
else:
    tamanho_parcela = None
    area_inventario = st.sidebar.number_input(
        "Tamanho da área do inventário (ha)",
        min_value=0.1, value=1.0
    )

# Converter o tipo de inventário para o formato esperado pelo R
tipo_inventario_r = "amostragem" if tipo_inventario == "Amostragem por parcelas" else "censo"
tipo_analise_r = tipo_analise if tipo_analise else "N/A"
tamanho_parcela_r = tamanho_parcela if tamanho_parcela else 0
tamanho_area_r = area_inventario if area_inventario else 0

# Criando a Interface
st.title("Gerador de Relatórios Ambientais")
st.write("Faça upload de um arquivo Excel contendo os dados do inventário florestal.")

uploaded_file = st.file_uploader("Envie seu arquivo", type=["xlsx"])
if uploaded_file is not None:
    df = processar_dados(uploaded_file)
    st.write("Prévia dos dados:")
    st.dataframe(df.head())
    
    if st.button("Gerar Relatório"):
        abundancias = ','.join(map(str, df.groupby('Espécie')['Diâmetro (cm)'].sum().tolist()))
        resultados_r = rodar_analise_r(abundancias, "dados_inventario.xlsx", 30, tamanho_area_r, tipo_inventario_r, tipo_analise_r, tamanho_parcela_r, tamanho_area_r, estratos_info)
        st.write("Resultados das Análises Estatísticas (R):")
        st.text(resultados_r)
