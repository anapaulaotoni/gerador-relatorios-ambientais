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
    
    # Objetivo da Intervenção Ambiental
    with st.expander("📌 Objetivo da Intervenção Ambiental"):
        st.markdown("### Selecione as Intervenções e Preencha os Detalhes")
        
        opcoes_intervencao = [
            "Supressão de vegetação nativa", "Intervenção em APPs", "Supressão de sub-bosque", 
            "Manejo sustentável", "Destoca", "Corte de árvores isoladas", "Supressão de eucaliptos", 
            "Aproveitamento de material lenhoso"
        ]
        
        intervencoes_selecionadas = {}
        areas_intervencao = {}
        individuos_intervencao = {}
        
        # Criando uma tabela organizada
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown("#### Tipo de Intervenção")
        with col2:
            st.markdown("#### Área (ha)")
        with col3:
            st.markdown("#### Nº de Indivíduos")
        
        for opcao in opcoes_intervencao:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                intervencoes_selecionadas[opcao] = st.checkbox(opcao)
            with col2:
                if intervencoes_selecionadas[opcao]:
                    areas_intervencao[opcao] = st.number_input(f"", min_value=0.1, value=1.0, key=f"area_{opcao}")
            with col3:
                if opcao in ["Corte de árvores isoladas", "Supressão de eucaliptos"] and intervencoes_selecionadas[opcao]:
                    individuos_intervencao[opcao] = st.number_input(f"", min_value=1, value=10, key=f"ind_{opcao}")
