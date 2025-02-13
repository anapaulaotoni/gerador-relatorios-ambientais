import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from io import BytesIO
import base64
import os
import scipy.stats as stats

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

def gerar_perfil_esquematico(df):
    """Gera um gráfico de perfil esquemático da floresta."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Criando distribuição aleatória para posição das árvores
    np.random.seed(42)
    df['x_pos'] = np.random.uniform(0, 10, df.shape[0])
    
    # Desenhando árvores como círculos proporcionais
    for _, row in df.iterrows():
        circle = plt.Circle((row['x_pos'], 0), row['Diâmetro (cm)']/50, color='green', alpha=0.7)
        ax.add_patch(circle)
        ax.plot([row['x_pos'], row['x_pos']], [0, row['Altura (m)']], color='brown', linewidth=2)
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, df['Altura (m)'].max() + 2)
    ax.set_xlabel("Posição das Árvores")
    ax.set_ylabel("Altura (m)")
    ax.set_title("Perfil Esquemático da Comunidade Florestal")
    ax.grid(False)
    
    plt.savefig("perfil_esquematico.png", bbox_inches='tight', dpi=300)
    return "perfil_esquematico.png"

def gerar_relatorio(df, estatisticas):
    """Gera um relatório em Word com os resultados, incluindo gráficos."""
    doc = Document()
    doc.add_heading('Relatório de Inventário Florestal', level=1)
    doc.add_paragraph("Este relatório apresenta os resultados do inventário florestal realizado.")
    doc.add_heading('1. Estatísticas Gerais', level=2)
    for col in estatisticas.index:
        doc.add_paragraph(f"{col}: {estatisticas.loc[col, 'mean']:.2f}")
    
    # Adicionar Perfil Esquemático
    perfil_path = gerar_perfil_esquematico(df)
    doc.add_picture(perfil_path, width=5000000, height=3000000)
    
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
    
    st.write("### Perfil Esquemático da Comunidade Florestal")
    perfil_path = gerar_perfil_esquematico(df)
    st.image(perfil_path, caption="Perfil Esquemático", use_container_width=True)
    
    if st.button("Gerar Relatório"):
        relatorio_content = gerar_relatorio(df, estatisticas)
        st.markdown(download_link(relatorio_content, "Relatorio_Inventario.docx", "📄 Baixar Relatório"), unsafe_allow_html=True)
