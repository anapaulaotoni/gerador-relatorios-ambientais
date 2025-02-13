import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from io import BytesIO
import base64
import os

def processar_dados(uploaded_file):
    """Processa os dados do arquivo e gera estatísticas."""
    df = pd.read_excel(uploaded_file)
    df = df.rename(columns={"scientific.name": "Espécie", "CAP": "Diâmetro (cm)", "HT": "Altura (m)"})
    df['Volume (m³)'] = np.pi * (df['Diâmetro (cm)'] / 200) ** 2 * df['Altura (m)']
    estatisticas = df.describe().T
    return df, estatisticas

def gerar_relatorio(df, estatisticas):
    """Gera um relatório em Word com os resultados."""
    doc = Document()
    doc.add_heading('Relatório de Inventário Florestal', level=1)
    doc.add_paragraph("Este relatório apresenta os resultados do inventário florestal realizado.")
    doc.add_heading('1. Estatísticas Gerais', level=2)
    for col in estatisticas.index:
        doc.add_paragraph(f"{col}: {estatisticas.loc[col, 'mean']:.2f}")
    
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
    
    if st.button("Gerar Relatório"):
        relatorio_content = gerar_relatorio(df, estatisticas)
        st.markdown(download_link(relatorio_content, "Relatorio_Inventario.docx", "📄 Baixar Relatório"), unsafe_allow_html=True)
