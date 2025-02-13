import streamlit as st
from docx import Document
from io import BytesIO
import geopandas as gpd

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
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }}
    .styled-table th, .styled-table td {{
        padding: 10px;
        border: 1px solid #ddd;
    }}
    .styled-table th {{
        background-color: {primary_color};
        color: white;
        text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# Estado da página
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# Página inicial
if st.session_state.pagina == "inicio":
    st.markdown("<h1 class='stTitle'>🌿 Gerador de Relatórios Ambientais</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='stHeader'>Automatize a criação de relatórios ambientais com análises fitossociológicas e estruturais.</h2>", unsafe_allow_html=True)
    if st.button("🚀 Iniciar Elaboração"):
        st.session_state.pagina = "dados_gerais"
        st.experimental_rerun()

# Dados Gerais
elif st.session_state.pagina == "dados_gerais":
    st.markdown("<h2 class='stHeader'>📌 Informações Gerais</h2>", unsafe_allow_html=True)
    nome_projeto = st.text_input("Nome do Projeto", "Inserir")
    responsavel = st.text_input("Responsável Técnico", "Inserir")
    data = st.date_input("Data do Relatório")

    # Localização do Projeto (Estado e Município)
    estado = st.selectbox("Selecione o Estado", ["Selecione", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
    municipio = st.text_input("Município do Projeto", "Inserir")
    
    if st.button("Avançar para Dados do Requerente"):
        if nome_projeto and responsavel and data and estado != "Selecione" and municipio:
            st.session_state.pagina = "dados_requerente"
            st.experimental_rerun()
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios antes de avançar.")

# Dados do Requerente
elif st.session_state.pagina == "dados_requerente":
    st.markdown("<h2 class='stHeader'>📌 Dados do Requerente ou Empreendedor</h2>", unsafe_allow_html=True)
    
    # Dados do Empreendedor
    nome_razao = st.text_input("Nome/Razão Social do Empreendedor")
    cnpj = st.text_input("CNPJ do Empreendedor")
    endereco = st.text_input("Endereço do Empreendedor")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")

    # Dados do Requerente
    nome_requerente = st.text_input("Nome/Razão Social do Requerente")
    cnpj_requerente = st.text_input("CNPJ do Requerente")
    endereco_requerente = st.text_input("Endereço do Requerente")
    
    if st.button("Avançar para Dados do Proprietário do Imóvel"):
        if nome_razao and cnpj and endereco and telefone and email:
            st.session_state.pagina = "dados_proprietario"
            st.experimental_rerun()
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios antes de avançar.")

    if st.button("Voltar para Dados Gerais"):
        st.session_state.pagina = "dados_gerais"
        st.experimental_rerun()

# Dados do Proprietário do Imóvel
elif st.session_state.pagina == "dados_proprietario":
    st.markdown("<h2 class='stHeader'>📌 Dados do Proprietário do Imóvel</h2>", unsafe_allow_html=True)
    
    denominacao_imovel = st.text_input("Denominação do Imóvel")
    proprietario = st.text_input("Proprietário")
    cnpj_proprietario = st.text_input("CNPJ do Proprietário")
    
    if st.button("Avançar para Dados do Imóvel Rural"):
        if denominacao_imovel and proprietario and cnpj_proprietario:
            st.session_state.pagina = "dados_imovel"
            st.experimental_rerun()
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios antes de avançar.")

    if st.button("Voltar para Dados do Requerente"):
        st.session_state.pagina = "dados_requerente"
        st.experimental_rerun()

# Dados do Imóvel Rural
elif st.session_state.pagina == "dados_imovel":
    st.markdown("<h2 class='stHeader'>📌 Dados do Imóvel Rural e Empreendimento</h2>", unsafe_allow_html=True)
    
    denominacao_imovel_rural = st.text_input("Denominação do Imóvel")
    municipio_imovel = st.text_input("Município")
    estado_imovel = st.selectbox("Estado", ["Selecione", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
    cep_imovel = st.text_input("CEP")
    matricula_imovel = st.text_input("Matrícula do Imóvel")
    area_imovel = st.number_input("Área da Propriedade (ha)", min_value=0.1)
    car_imovel = st.text_input("CAR")
    atividades_imovel = st.text_area("Atividades Desenvolvidas no Empreendimento")
    
    if st.button("Avançar para Dados da Empresa Responsável"):
        if denominacao_imovel_rural and municipio_imovel and estado_imovel != "Selecione" and cep_imovel and matricula_imovel and area_imovel > 0:
            st.session_state.pagina = "dados_empresa"
            st.experimental_rerun()
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios antes de avançar.")

    if st.button("Voltar para Dados do Proprietário"):
        st.session_state.pagina = "dados_proprietario"
        st.experimental_rerun()

# Dados da Empresa Responsável
elif st.session_state.pagina == "dados_empresa":
    st.markdown("<h2 class='stHeader'>📌 Dados da Empresa Responsável pela Elaboração do PIA e Equipe Técnica</h2>", unsafe_allow_html=True)
    
    nome_empresa = st.text_input("Nome/Razão Social")
    cnpj_empresa = st.text_input("CNPJ")
    inscricao_estadual_empresa = st.text_input("Inscrição Estadual")
    endereco_empresa = st.text_input("Endereço")
    municipio_empresa = st.text_input("Município")
    estado_empresa = st.selectbox("Estado", ["Selecione", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "
