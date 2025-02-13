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

# Paleta de cores personalizada
primary_color = "#8FC9CB"
secondary_color = "#97C1A9"
background_color = "#CCE2CB"
accent_color = "#5FA37A"
text_color = "#2E4053"

# CSS para melhoria da interface
st.markdown(f"""
    <style>
    .main {{
        background-color: {background_color};
        padding: 20px;
    }}
    .block-container {{
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {accent_color};
    }}
    .stTitle {{
        color: {text_color};
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }}
    .stHeader {{
        color: {secondary_color};
        font-size: 24px;
        text-align: center;
    }}
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
    # Formulário Inicial
    st.markdown("<h2 class='stHeader'>📌 Informações Gerais</h2>", unsafe_allow_html=True)
    
    # Dados do Requerente ou Empreendedor
    with st.expander("📌 Dados do Requerente ou Empreendedor"):
        nome_requerente = st.text_input("Nome/Razão Social")
        cnpj_requerente = st.text_input("CNPJ")
        endereco_requerente = st.text_area("Endereço")
        contato_requerente = st.text_input("Nome do Contato")
        telefone_requerente = st.text_input("Telefone")
        email_requerente = st.text_input("E-mail")
    
    # Dados do Proprietário do Imóvel
    with st.expander("📌 Dados do Proprietário do Imóvel"):
        nome_proprietario = st.text_input("Nome do Proprietário")
        cnpj_proprietario = st.text_input("CNPJ do Proprietário")
    
    # Dados do Imóvel
    with st.expander("📌 Dados do Imóvel"):
        denominacao_imovel = st.text_input("Denominação do Imóvel")
        municipio_imovel = st.text_input("Município")
        area_propriedade = st.number_input("Área da Propriedade (ha)", min_value=0.1, value=1.0)
        car_imovel = st.text_input("Cadastro Ambiental Rural (CAR)")
    
    # Objetivo da Intervenção Ambiental
    with st.expander("📌 Objetivo da Intervenção Ambiental"):
        st.markdown("### Selecione as Intervenções")
        intervencoes_selecionadas = []
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            for chave in ["Supressão de vegetação nativa", "Intervenção em APPs", "Supressão de sub-bosque", "Manejo sustentável", "Destoca", "Corte de árvores isoladas", "Supressão de eucaliptos", "Aproveitamento de material lenhoso"]:
                if st.checkbox(chave):
                    intervencoes_selecionadas.append(chave)
        
        areas_intervencao = {}
        individuos_intervencao = {}
        
        with col2:
            for chave in intervencoes_selecionadas:
                areas_intervencao[chave] = st.number_input(f"Área (ha) para {chave}", min_value=0.1, value=1.0)
        
        with col3:
            for chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                if chave in intervencoes_selecionadas:
                    individuos_intervencao[chave] = st.number_input(f"Indivíduos para {chave}", min_value=1, value=10)
        for chave in intervencoes.keys():
            intervencoes[chave] = st.checkbox(chave)
            if intervencoes[chave]:
                col1, col2 = st.columns([1, 1])
                with col1:
                    areas_intervencao[chave] = st.number_input(f"Área requerida para {chave} (ha)", min_value=0.1, value=1.0)
                with col2:
                    if chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                        individuos_intervencao[chave] = st.number_input(f"Número de indivíduos para {chave}", min_value=1, value=10)
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                intervencoes[chave] = st.checkbox(chave)
            with col2:
                if intervencoes[chave]:
                    areas_intervencao[chave] = st.number_input(f"Área (ha) para {chave}", min_value=0.1, value=1.0)
            with col3:
                if chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"] and intervencoes[chave]:
                    individuos_intervencao[chave] = st.number_input(f"Indivíduos para {chave}", min_value=1, value=10)
            with st.expander(chave):
                intervencoes[chave] = st.checkbox(f"Selecionar {chave}")
                if intervencoes[chave]:
                    areas_intervencao[chave] = st.number_input(f"Área requerida para {chave} (ha)", min_value=0.1, value=1.0)
                    if chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                        individuos_intervencao[chave] = st.number_input(f"Número de indivíduos para {chave}", min_value=1, value=10)
                intervencoes[chave] = st.checkbox(chave)
        
        with col2:
            for chave, selecionado in intervencoes.items():
                if selecionado:
                    areas_intervencao[chave] = st.number_input(f"Área (ha) para {chave}", min_value=0.1, value=1.0)
        
        with col3:
            for chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                if intervencoes.get(chave, False):
                    individuos_intervencao[chave] = st.number_input(f"Indivíduos para {chave}", min_value=1, value=10)
            if selecionado:
                areas_intervencao[chave] = st.number_input(f"Área requerida para {chave} (ha)", min_value=0.1, value=1.0)
                if chave in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                    individuos_intervencao[chave] = st.number_input(f"Número de indivíduos para {chave}", min_value=1, value=10)
    
    # Caracterização do Meio Biótico
    with st.expander("📌 Caracterização do Meio Biótico"):
        bioma = st.selectbox("Selecione o bioma:", ["Amazônia", "Mata Atlântica", "Cerrado", "Caatinga", "Pantanal", "Pampa"])
        flora_upload = st.file_uploader("Upload da Lista Florística", type=["xlsx", "csv"])
        fauna_upload = st.file_uploader("Upload da Lista Faunística", type=["xlsx", "csv"])
    
    # Caracterização do Meio Abiótico
    with st.expander("📌 Caracterização do Meio Abiótico"):
        clima_upload = st.file_uploader("Upload de Dados Climáticos")
        solos_upload = st.file_uploader("Upload de Relatório Pedológico")
        hidrografia_upload = st.file_uploader("Upload de Mapas Hidrográficos")
        topografia_upload = st.file_uploader("Upload de Modelo Digital de Terreno")
    
    # Botão para avançar
    if st.button("Avançar para o Inventário Florestal"):
        st.session_state.inicio = "inventario"
        st.rerun()
    
    if "inventario" in st.session_state:
        # Inserindo a parte do inventário florestal já existente no código
        st.markdown("<h2 class='stHeader'>📌 Tipo de Inventário</h2>", unsafe_allow_html=True)
        tipo_inventario = st.selectbox("Selecione o tipo de inventário:", ["Amostragem por parcelas", "Censo florestal"])
        
        if tipo_inventario == "Amostragem por parcelas":
            tipo_analise = st.selectbox("Escolha o tipo de análise:", ["Casual Simples", "Estratificada"])
            tamanho_parcela = st.number_input("📏 Tamanho da parcela (m²)", min_value=1, value=100)
            area_inventario = st.number_input("🌍 Tamanho da área do inventário (ha)", min_value=0.1, value=1.0)
        
        st.markdown("<h2 class='stHeader'>📂 Enviar Arquivo de Dados</h2>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Faça upload do arquivo Excel contendo os dados do inventário florestal", type=["xlsx"])
