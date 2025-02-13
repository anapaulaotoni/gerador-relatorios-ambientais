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

def rodar_analise_r(abundancias):
    """Executa o script R e captura os resultados."""
    resultado = subprocess.run(["Rscript", "analises_florestais.R", abundancias], capture_output=True, text=True)
    return resultado.stdout
def gerar_perfil_esquematico(df):
    """Gera um gráfico de perfil esquemático da floresta com nomes ajustados."""
    especies = df.groupby('Espécie').agg({'Altura (m)': 'mean', 'Diâmetro (cm)': 'mean'}).reset_index()
    especies['Espécie'] = especies['Espécie'].apply(formatar_nome_cientifico)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    np.random.seed(42)
    especies['x_pos'] = np.linspace(0, 10, len(especies))
    
    text_objects = []
    for _, row in especies.iterrows():
        ellipse = plt.Circle((row['x_pos'], row['Altura (m)']), row['Diâmetro (cm)']/30, color='green', alpha=0.7)
        ax.add_patch(ellipse)
        ax.plot([row['x_pos'], row['x_pos']], [0, row['Altura (m)']], color='brown', linewidth=2)
        text_objects.append(ax.text(row['x_pos'], row['Altura (m)'] + 0.5, row['Espécie'], fontsize=8, fontstyle='italic', ha='center'))
    
    adjust_text(text_objects, arrowprops=dict(arrowstyle='-', color='black'))
    
    ax.set_xlim(-1, 11)
    ax.set_ylim(0, especies['Altura (m)'].max() + 2)
    ax.set_xlabel("Posição das Árvores")
    ax.set_ylabel("Altura (m)")
    ax.set_title("Perfil Esquemático da Comunidade Florestal")
    ax.grid(False)
    
    plt.savefig("perfil_esquematico.png", bbox_inches='tight', dpi=300)
    return "perfil_esquematico.png"

def gerar_relatorio(df):
    """Gera um relatório em Word com os resultados, incluindo gráficos."""
    doc = Document()
    doc.add_heading('Relatório de Inventário Florestal', level=1)
    doc.add_paragraph("Este relatório apresenta os resultados do inventário florestal realizado.")
    
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
    df = processar_dados(uploaded_file)
    st.write("Prévia dos dados:")
    st.dataframe(df.head())
    
    st.write("### Perfil Esquemático da Comunidade Florestal")
    perfil_path = gerar_perfil_esquematico(df)
    st.image(perfil_path, caption="Perfil Esquemático", use_container_width=True)
    
    if st.button("Gerar Relatório"):
        relatorio_content = gerar_relatorio(df)
        st.markdown(download_link(relatorio_content, "Relatorio_Inventario.docx", "📄 Baixar Relatório"), unsafe_allow_html=True)
