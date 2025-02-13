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
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    .styled-table th {
        background-color: {primary_color};
        color: white;
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
        
        tabela_html = """
        <table class='styled-table'>
            <tr>
                <th>Tipo de Intervenção</th>
                <th>Área (ha)</th>
                <th>Nº de Indivíduos</th>
            </tr>
        """
        
        for opcao in opcoes_intervencao:
            intervencoes_selecionadas[opcao] = st.checkbox(opcao)
            area_input = "-"
            individuos_input = "-"
            
            if intervencoes_selecionadas[opcao]:
                area_input = st.number_input(f"", min_value=0.1, value=1.0, key=f"area_{opcao}")
                if opcao in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                    individuos_input = st.number_input(f"", min_value=1, value=10, key=f"ind_{opcao}")
            
            tabela_html += f"<tr><td>{opcao}</td><td>{area_input}</td><td>{individuos_input}</td></tr>"
        
        tabela_html += "</table>"
        st.markdown(tabela_html, unsafe_allow_html=True)
