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
        st.rerun()

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
        st.session_state.pagina = "dados_requerente"
        st.rerun()

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
        st.session_state.pagina = "dados_proprietario"
        st.rerun()

    if st.button("Voltar para Dados Gerais"):
        st.session_state.pagina = "dados_gerais"
        st.rerun()

# Dados do Proprietário do Imóvel
elif st.session_state.pagina == "dados_proprietario":
    st.markdown("<h2 class='stHeader'>📌 Dados do Proprietário do Imóvel</h2>", unsafe_allow_html=True)
    
    denominacao_imovel = st.text_input("Denominação do Imóvel")
    proprietario = st.text_input("Proprietário")
    cnpj_proprietario = st.text_input("CNPJ do Proprietário")
    
    if st.button("Avançar para Dados do Imóvel Rural"):
        st.session_state.pagina = "dados_imovel"
        st.rerun()

    if st.button("Voltar para Dados do Requerente"):
        st.session_state.pagina = "dados_requerente"
        st.rerun()

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
        st.session_state.pagina = "dados_empresa"
        st.rerun()

    if st.button("Voltar para Dados do Proprietário"):
        st.session_state.pagina = "dados_proprietario"
        st.rerun()

# Dados da Empresa Responsável
elif st.session_state.pagina == "dados_empresa":
    st.markdown("<h2 class='stHeader'>📌 Dados da Empresa Responsável pela Elaboração do PIA e Equipe Técnica</h2>", unsafe_allow_html=True)
    
    nome_empresa = st.text_input("Nome/Razão Social")
    cnpj_empresa = st.text_input("CNPJ")
    inscricao_estadual_empresa = st.text_input("Inscrição Estadual")
    endereco_empresa = st.text_input("Endereço")
    municipio_empresa = st.text_input("Município")
    estado_empresa = st.selectbox("Estado", ["Selecione", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
    cep_empresa = st.text_input("CEP")
    contato_empresa = st.text_input("Contato")
    cargo_empresa = st.text_input("Cargo")
    telefone_empresa = st.text_input("Telefone")
    email_empresa = st.text_input("E-mail")
    
    if st.button("Avançar para Identificação da Equipe"):
        st.session_state.pagina = "equipe_tecnica"
        st.rerun()

    if st.button("Voltar para Dados do Imóvel Rural"):
        st.session_state.pagina = "dados_imovel"
        st.rerun()

# Identificação da Equipe Responsável
elif st.session_state.pagina == "equipe_tecnica":
    st.markdown("<h2 class='stHeader'>📌 Identificação da Equipe Responsável pela Elaboração do Projeto</h2>", unsafe_allow_html=True)
    
    nome_profissional = st.text_input("Nome do Profissional")
    formacao_profissional = st.text_input("Formação Técnica")
    registro_profissional = st.text_input("Registro Profissional")
    responsabilidade_profissional = st.text_input("Responsabilidade")
    
    adicionar_profissional = st.checkbox("Adicionar outro profissional")
    
    if adicionar_profissional:
        nome_profissional_2 = st.text_input("Nome do 2º Profissional")
        formacao_profissional_2 = st.text_input("Formação Técnica do 2º Profissional")
        registro_profissional_2 = st.text_input("Registro Profissional do 2º Profissional")
        responsabilidade_profissional_2 = st.text_input("Responsabilidade do 2º Profissional")
    
    if st.button("Avançar para Dados do Responsável Técnico"):
        st.session_state.pagina = "responsavel_tecnico"
        st.rerun()

    if st.button("Voltar para Dados da Empresa Responsável"):
        st.session_state.pagina = "dados_empresa"
        st.rerun()

# Dados do Responsável Técnico
elif st.session_state.pagina == "responsavel_tecnico":
    st.markdown("<h2 class='stHeader'>📌 Dados do Responsável Técnico pelo Projeto de Intervenção Ambiental</h2>", unsafe_allow_html=True)
    
    nome_responsavel = st.text_input("Nome")
    cpf_responsavel = st.text_input("CPF")
    email_responsavel = st.text_input("E-mail")
    telefone_responsavel = st.text_input("Telefone(s)")
    formacao_responsavel = st.text_input("Formação")
    registro_conselho_responsavel = st.text_input("Nº de registro em conselho de classe")
    numero_art_responsavel = st.text_input("Nº ART")
    ctf_aida_responsavel = st.text_input("CTF/AIDA")
    
    if st.button("Avançar para Objetivo da Intervenção Ambiental"):
        st.session_state.pagina = "objetivo_intervencao"
        st.rerun()

    if st.button("Voltar para Identificação da Equipe"):
        st.session_state.pagina = "equipe_tecnica"
        st.rerun()

 #Objetivo da Intervenção Ambiental
# Objetivo da Intervenção Ambiental
elif st.session_state.pagina == "objetivo_intervencao":
    st.markdown("<h2 class='stHeader'>📌 Objetivo da Intervenção Ambiental</h2>", unsafe_allow_html=True)
    
    st.markdown("### Selecione as Intervenções e Preencha os Detalhes")
    
    # Opções de intervenções
    opcoes_intervencao = [
        "Supressão de vegetação nativa", 
        "Intervenção em APPs", 
        "Supressão de sub-bosque", 
        "Manejo sustentável", 
        "Destoca", 
        "Corte de árvores isoladas", 
        "Supressão de eucaliptos", 
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
            area_input = st.number_input(f"Área (ha) - {opcao}", min_value=0.1, value=1.0, key=f"area_{opcao}")
            if opcao in ["Corte de árvores isoladas", "Supressão de eucaliptos"]:
                individuos_input = st.number_input(f"Nº de Indivíduos - {opcao}", min_value=1, value=10, key=f"ind_{opcao}")
        
        tabela_html += f"<tr><td>{opcao}</td><td>{area_input}</td><td>{individuos_input}</td></tr>"
    
    tabela_html += "</table>"
    st.markdown(tabela_html, unsafe_allow_html=True)
    
    # Verificar se o botão "Próximo" foi pressionado para avançar
    if st.button("Próximo"):
        # Se pelo menos uma intervenção for selecionada, avança para a próxima página
        if any(intervencoes_selecionadas.values()):
            st.session_state.pagina = "caracterizacao_meio_biotico"
            st.experimental_rerun()  # Isso vai recarregar a página e avançar para a próxima
        else:
            st.warning("Por favor, selecione pelo menos uma intervenção antes de avançar.")
    
    if st.button("Voltar para Dados do Responsável Técnico"):
        st.session_state.pagina = "responsavel_tecnico"
        st.experimental_rerun()  # Isso vai recarregar a página anterior

# Área de Preservação Permanente (APP)
elif st.session_state.pagina == "app":
    st.markdown("<h2 class='stHeader'>📌 Área de Preservação Permanente (APP)</h2>", unsafe_allow_html=True)
    
    # Pergunta se a área de intervenção está inserida em APP
    app_inserido = st.radio("A área de intervenção do projeto está inserida em Área de Preservação Permanente (APP)?", ["Selecione", "Sim", "Não"])
    
    # Condição para mostrar a área sobreposta se o usuário selecionar "Sim"
    if app_inserido == "Sim":
        area_app = st.number_input("Tamanho da área (ha) sobreposta com a área de intervenção", min_value=0.1)
    else:
        area_app = 0
    
    # Botões para avançar ou voltar
    if st.button("Avançar para Corredores Ecológicos"):
        # Verificando se o botão "Avançar" pode funcionar
        if app_inserido == "Sim" and area_app > 0:  # Verifica se a área foi preenchida
            st.session_state.pagina = "corredores_ecologicos"
            st.experimental_rerun()  # Isso vai recarregar a página e avançar para a próxima
        elif app_inserido == "Não":  # Se a resposta for "Não", avança para a próxima página
            st.session_state.pagina = "corredores_ecologicos"
            st.experimental_rerun()  # Isso vai recarregar a página e avançar para a próxima
        else:
            st.warning("Por favor, insira os dados necessários antes de avançar.")
    
    # Botão de Voltar
    if st.button("Voltar para Dados do Responsável Técnico"):
        st.session_state.pagina = "responsavel_tecnico"
        st.experimental_rerun()  # Isso vai recarregar a página anterior



# Reserva da Biosfera da Mata Atlântica
elif st.session_state.pagina == "reserva_biosfera_mata_atlantica":
    st.markdown("<h2 class='stHeader'>📌 Reserva da Biosfera da Mata Atlântica</h2>", unsafe_allow_html=True)
    reserva_biosfera = st.radio("A área de intervenção do projeto está inserida na reserva ou seu entorno?", ["Sim", "Não"])
    if reserva_biosfera == "Sim":
        area_nucleo = st.text_input("Área - Núcleo")
        zona_amortecimento = st.text_input("Zona de Amortecimento")
        zona_transicao = st.text_input("Zona de Transição")
    
    if st.button("Avançar para Reserva da Biosfera da Serra do Espinhaço"):
        st.session_state.pagina = "reserva_biosfera_serra_espinhaco"
        st.rerun()

# Reserva da Biosfera da Serra do Espinhaço
elif st.session_state.pagina == "reserva_biosfera_serra_espinhaco":
    st.markdown("<h2 class='stHeader'>📌 Reserva da Biosfera da Serra do Espinhaço</h2>", unsafe_allow_html=True)
    reserva_biosfera_serra = st.radio("A área de intervenção do projeto está inserida na reserva ou seu entorno?", ["Sim", "Não"])
    if reserva_biosfera_serra == "Sim":
        area_nucleo_serra = st.text_input("Área - Núcleo")
        zona_amortecimento_serra = st.text_input("Zona de Amortecimento")
        zona_transicao_serra = st.text_input("Zona de Transição")
    
    if st.button("Avançar para Sítios Ramsar"):
        st.session_state.pagina = "sitos_ramsar"
        st.rerun()

# Sítios Ramsar
elif st.session_state.pagina == "sitos_ramsar":
    st.markdown("<h2 class='stHeader'>📌 Sítios Ramsar</h2>", unsafe_allow_html=True)
    sitios_ramsar = st.radio("A área de intervenção do projeto está inserida em Sítios Ramsar?", ["Sim", "Não"])
    if sitios_ramsar == "Sim":
        nome_sitio = st.text_input("Nome do Sítio Ramsar")
    
    if st.button("Avançar para Hidrografia"):
        st.session_state.pagina = "hidrografia"
        st.rerun()

# Hidrografia
elif st.session_state.pagina == "hidrografia":
    st.markdown("<h2 class='stHeader'>📌 Hidrografia</h2>", unsafe_allow_html=True)
    bacia_hidrografica = st.text_input("Bacia Hidrográfica")
    subbacia_hidrografica = st.text_input("Subbacia Hidrográfica")
    
    if st.button("Avançar para Inventário Florestal"):
        st.session_state.pagina = "inventario_florestal"
        st.rerun()

# Inventário Florestal
elif st.session_state.pagina == "inventario_florestal":
    st.markdown("<h2 class='stHeader'>📌 Inventário Florestal</h2>", unsafe_allow_html=True)
    tipo_inventario = st.selectbox("Tipo de Inventário", ["Censo Florestal", "Inventário por Amostragem"])
    
    if tipo_inventario == "Censo Florestal":
        area_inventario = st.number_input("Tamanho da área em hectares")
        formula_inventario = st.text_input("Fórmula a ser utilizada")
    elif tipo_inventario == "Inventário por Amostragem":
        tamanho_parcela = st.number_input("Tamanho da parcela (ha)")
        dimensao_parcela = st.text_input("Dimensões da parcela (comprimento x largura)")
        area_inventario_amostragem = st.number_input("Tamanho da área do inventário")
        tipo_analise = st.selectbox("Tipo de Análise", ["Casual Simples", "Casual Estratificada"])
        
        if tipo_analise == "Casual Simples":
            formula_volume = st.text_input("Fórmula do volume")
        elif tipo_analise == "Casual Estratificada":
            num_estrato = st.number_input("Número de estratos")
            nome_estrato = st.text_input("Nome do estrato")
            tamanho_area_estrato = st.number_input("Tamanho da área do estrato")
            formula_estrato = st.text_input("Fórmula do estrato")
    
    if st.button("Avançar para Enviar Resultados"):
        st.session_state.pagina = "enviar_resultados"
        st.rerun()

# Enviar Resultados
elif st.session_state.pagina == "enviar_resultados":
    st.markdown("<h2 class='stHeader'>📌 Enviar Resultados para Análise</h2>", unsafe_allow_html=True)
    st.write("Por favor, envie os dados para que possamos rodar os resultados e analisar o inventário florestal.")
 
