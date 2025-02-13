import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from io import BytesIO
import base64
import os

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
    estatisticas = df.describe().T
    return df, estatisticas

def gerar_relatorio(df, estatisticas):
    """Gera um relatório em Word com os resultados, incluindo gráficos."""
    doc = Document()
    doc.add_heading('Relatório de Inventário Florestal', level=1)
    doc.add_paragraph("Este relatório apresenta os resultados do inventário florestal realizado.")
    doc.add_heading('1. Estatísticas Gerais', level=2)
    for col in estatisticas.index:
        doc.add_paragraph(f"{col}: {estatisticas.loc[col, 'mean']:.2f}")
    
    # Gerar gráficos e salvar como imagens temporárias
    plt.style.use('default')  # Fundo branco
    
    fig, ax = plt.subplots(figsize=(6, 4))
    df['Diâmetro (cm)'].hist(bins=15, color='green', alpha=0.7, edgecolor='black')
    df['Diâmetro (cm)'].plot(kind='kde', ax=ax, secondary_y=False, color='red')
    plt.xlabel("Diâmetro (cm)")
    plt.ylabel("Frequência")
    plt.title("Distribuição Diamétrica")
    diametro_path = "diametro_plot.png"
    plt.savefig(diametro_path, bbox_inches='tight', dpi=300)
    doc.add_picture(diametro_path, width=5000000, height=3000000)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    especies_formatadas = df['Espécie'].value_counts().nlargest(10)
    especies_formatadas.index = especies_formatadas.index.map(formatar_nome_cientifico)
    especies_formatadas.plot(kind='bar', color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel("Espécie", fontsize=10, fontstyle='italic')
    plt.ylabel("Quantidade")
    plt.title("Abundância de Espécies")
    plt.xticks(rotation=45, ha='right', fontsize=10, fontstyle='italic')
    especies_path = "especies_plot.png"
    plt.savefig(especies_path, bbox_inches='tight', dpi=300)
    doc.add_picture(especies_path, width=5000000, height=3000000)
    
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()

def download_link(content, filename, label):
    """Cria um link de download para o arquivo gerado."""
    b64 = base64.b64encode(content).decode()
    href = f'<a href="data:file/docx;base64,{b64}" download="{filename}">{label}</a>'
    return href

# Criando a Interface
st.title("Gerador de Relatórios Ambientais")
st.write("Faça upload de um arquivo Excel contendo os dados do inventário florestal.")

uploaded_file = st.file_uploader("Envie seu arquivo", type=["xlsx"])
if uploaded_file is not None:
    df, estatisticas = processar_dados(uploaded_file)
    st.write("Prévia dos dados:")
    st.dataframe(df.head())
    
    st.write("Estatísticas Calculadas:")
    st.dataframe(estatisticas)
    
    # Adicionar visualização de gráficos no Streamlit
    st.write("### Distribuição dos Diâmetros das Árvores")
    fig, ax = plt.subplots(figsize=(6, 4))
    df['Diâmetro (cm)'].hist(bins=15, color='green', alpha=0.7, edgecolor='black')
    df['Diâmetro (cm)'].plot(kind='kde', ax=ax, secondary_y=False, color='red')
    plt.xlabel("Diâmetro (cm)")
    plt.ylabel("Frequência")
    plt.title("Distribuição Diamétrica")
    st.pyplot(fig)
    
    st.write("### Abundância de Espécies")
    fig, ax = plt.subplots(figsize=(6, 4))
    especies_formatadas = df['Espécie'].value_counts().nlargest(10)
    especies_formatadas.index = especies_formatadas.index.map(formatar_nome_cientifico)
    especies_formatadas.plot(kind='bar', color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel("Espécie", fontsize=10, fontstyle='italic')
    plt.ylabel("Quantidade")
    plt.title("Abundância de Espécies")
    plt.xticks(rotation=45, ha='right', fontsize=10, fontstyle='italic')
    st.pyplot(fig)
    
    if st.button("Gerar Relatório"):
        relatorio_content = gerar_relatorio(df, estatisticas)
        st.markdown(download_link(relatorio_content, "Relatorio_Inventario.docx", "📄 Baixar Relatório"), unsafe_allow_html=True)
