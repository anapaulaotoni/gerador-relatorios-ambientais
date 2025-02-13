import streamlit as st
from docx import Document
from io import BytesIO
import zipfile
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

if st.session_state.pagina == "inicio":
    st.markdown("<h1 class='stTitle'>🌿 Gerador de Relatórios Ambientais</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='stHeader'>Automatize a criação de relatórios ambientais com análises fitossociológicas e estruturais.</h2>", unsafe_allow_html=True)
    if st.button("🚀 Iniciar Elaboração"):
        st.session_state.pagina = "dados_gerais"
        st.rerun()

elif st.session_state.pagina == "dados_gerais":
    st.markdown("<h2 class='stHeader'>📌 Informações Gerais</h2>", unsafe_allow_html=True)
    nome_projeto = st.text_input("Nome do Projeto", "Inserir")
    responsavel = st.text_input("Responsável Técnico", "Inserir")
    data = st.date_input("Data do Relatório")
    localizacao = st.text_area("Localização do Projeto", "Inserir")
    
    if st.button("Avançar para Dados do Requerente"):
        st.session_state.pagina = "dados_requerente"
        st.rerun()

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
    
    # Botões para navegar entre as páginas
    if st.button("Avançar para Objetivo da Intervenção Ambiental"):
        st.session_state.pagina = "objetivo_intervencao"
        st.rerun()

elif st.session_state.pagina == "objetivo_intervencao":
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
    
    if st.button("Próximo"):
        st.session_state.pagina = "detalhes_adicionais"
        st.rerun()

elif st.session_state.pagina == "detalhes_adicionais":
    st.markdown("<h2 class='stHeader'>📌 Informações Adicionais</h2>", unsafe_allow_html=True)
    descricao_projeto = st.text_area("Descrição do Projeto", "Inserir")
    metodologia = st.text_area("Metodologia Utilizada", "Inserir")
    conclusao = st.text_area("Conclusão e Considerações Finais", "Inserir")
    
    if st.button("Finalizar e Gerar Relatório"):
        st.session_state.pagina = "finalizar"
        st.rerun()

elif st.session_state.pagina == "finalizar":
    st.markdown("<h2 class='stHeader'>✅ Relatório Gerado com Sucesso!</h2>", unsafe_allow_html=True)
    st.write("Baixe seu relatório abaixo.")

    # Função para gerar o relatório DOCX
    def gerar_relatorio():
        doc = Document()
        doc.add_heading('Relatório Ambiental', 0)

        # Informações Gerais
        doc.add_heading('Informações Gerais', level=1)
        doc.add_paragraph(f"Nome do Projeto: {nome_projeto}")
        doc.add_paragraph(f"Responsável Técnico: {responsavel}")
        doc.add_paragraph(f"Data do Relatório: {data}")
        doc.add_paragraph(f"Localização do Projeto: {localizacao}")

        # Dados do Requerente
        doc.add_heading('Dados do Requerente ou Empreendedor', level=1)
        doc.add_paragraph(f"Nome/Razão Social do Empreendedor: {nome_razao}")
        doc.add_paragraph(f"CNPJ do Empreendedor: {cnpj}")
        doc.add_paragraph(f"Endereço do Empreendedor: {endereco}")
        doc.add_paragraph(f"Telefone: {telefone}")
        doc.add_paragraph(f"E-mail: {email}")

        # Objetivo da Intervenção Ambiental
        doc.add_heading('Objetivo da Intervenção Ambiental', level=1)
        for opcao in opcoes_intervencao:
            if intervencoes_selecionadas[opcao]:
                doc.add_paragraph(f"- {opcao}: Área = {areas_intervencao.get(opcao, '-')}, Nº de Indivíduos = {individuos_intervencao.get(opcao, '-')}")
        
        # Informações Adicionais
        doc.add_heading('Informações Adicionais', level=1)
        doc.add_paragraph(f"Descrição do Projeto: {descricao_projeto}")
        doc.add_paragraph(f"Metodologia Utilizada: {metodologia}")
        doc.add_paragraph(f"Conclusão: {conclusao}")

        # Salvando o documento em um arquivo BytesIO
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        return buffer

    # Exibindo o botão para download
    buffer = gerar_relatorio()
    st.download_button(label="Download do Relatório", data=buffer, file_name="relatorio_ambiental.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
