import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io

###############################
# CONFIGURAÇÃO DA PÁGINA
###############################
st.set_page_config(page_title="Avaliação Transporte Pediátrico", layout="wide")

# Criação das abas: Passo 1 e Passo 2 – Avaliação do risco de transporte
abas = st.tabs(["Passo 1: Dados do doente", "Passo 2 – Avaliação do risco de transporte"])

#####################################
# PASSO 1: Dados do doente
#####################################
with abas[0]:
    st.title("Passo 1: Dados do doente")
    st.markdown("Insira os dados básicos do doente e do transporte.")
    
    with st.expander("Dados do doente", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_utente = st.text_input("Nome do utente *")
            # Idade: número inteiro sem decimais.
            idade = st.number_input("Idade", min_value=0, step=1)
            # Unidade de idade - aparece depois da idade.
            unidade_idade = st.selectbox("Unidade de idade", options=["Dias", "Meses", "Anos"], index=2)
            peso = st.number_input("Peso (kg) *", min_value=0.0, step=0.1, format="%.1f")
        with col2:
            diagnosticos = [
                "Pneumonia", "Choque séptico", "Insuficiência respiratória aguda",
                "Estado convulsivo", "Cardiopatia congénita", "Traumatismo craniano",
                "Bronquiolite", "Asma", "Sepse neonatal"
            ]
            opcoes_diagnostico = diagnosticos + ["Outro (escrever)"]
            diagnostico_selecionado = st.selectbox("Diagnóstico principal (autocompletar)", options=opcoes_diagnostico)
            if diagnostico_selecionado == "Outro (escrever)":
                diagnostico_final = st.text_input("Introduza o diagnóstico manualmente")
            else:
                diagnostico_final = diagnostico_selecionado

            data_transporte = st.date_input("Data do transporte *", value=datetime.now().date())
            hora_transporte = st.time_input("Hora do transporte *", value=datetime.now().time())
    
    if st.button("Submeter Dados do Doente", key="submeter_dados"):
        st.success("Dados do doente submetidos com sucesso!")
        st.markdown("### Resumo:")
        st.write(f"**Nome:** {nome_utente}")
        st.write(f"**Idade:** {idade} {unidade_idade}")
        st.write(f"**Peso:** {peso} kg")
        st.write(f"**Diagnóstico:** {diagnostico_final}")
        st.write(f"**Data do Transporte:** {data_transporte.strftime('%d/%m/%Y')}")
        st.write(f"**Hora do Transporte:** {hora_transporte.strftime('%H:%M')}")


#####################################
# PASSO 2 – Avaliação do risco de transporte
#####################################
with abas[1]:
    st.title("Passo 2 – Avaliação do risco de transporte")
    st.markdown("Preencha os parâmetros (médias das últimas 3 horas) para avaliar o risco do transporte:")
    
    ##############################
    # Seção 1: Avaliação Respiratória
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("1. Avaliação Respiratória")
    modalidade = st.selectbox("Modalidade ventilatória", 
              options=[
                  "Ventilação Mecânica Invasiva (VMI)", 
                  "Ventilação Não Invasiva (VNI)", 
                  "Oxigenoterapia de Alto Fluxo (OAF)", 
                  "Oxigênio Suplementar", 
                  "Ar ambiente"
              ])
    if modalidade == "Ventilação Mecânica Invasiva (VMI)":
        nivel_tubo = st.text_input("Nível do tubo Oro-traqueal")
        fixacao = st.radio("Fixação do tubo adequada", options=["Sim", "Não"])
        auscultacao = st.radio("Auscultação simétrica", options=["Sim", "Não"])
    elif modalidade == "Ventilação Não Invasiva (VNI)":
        vni_mod = st.selectbox("Modalidade", options=["CPAP", "BIPAP"])
        protecao_facial = st.radio("Placas de proteção facial", options=["Sim", "Não"])
        resp_dif_vni = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    elif modalidade == "Oxigenoterapia de Alto Fluxo (OAF)":
        fluxos = st.radio("Fluxos estão adequados", options=["Sim", "Não"])
        resp_dif_oaf = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    elif modalidade == "Oxigênio Suplementar":
        tipo_mascara = st.selectbox("Tipo de máscara", options=["Máscara de alto débito", "Máscara de Venturi", "Máscara simples", "O2 por óculos nasais"])
        resp_dif_sup = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    # "Ar ambiente": sem questões adicionais.
    fio2 = st.number_input("FiO₂ média das últimas 3h (%)", min_value=21, max_value=100, value=21)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Seção 2: Avaliação Hemodinâmica
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("2. Avaliação Hemodinâmica (médias das últimas 3h)")
    fc = st.number_input("Frequência cardíaca média (lpm)", min_value=0, step=1)
    pas = st.number_input("Pressão arterial sistólica (mmHg)", min_value=0, step=1)
    pad = st.number_input("Pressão arterial diastólica (mmHg)", min_value=0, step=1)
    pam = st.number_input("Pressão arterial média (mmHg)", min_value=0, step=1)
    satO2 = st.number_input("SatO₂ média (%)", min_value=0, max_value=100, step=1)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Seção 3: Infusões Vasoativas (mcg/kg/min)
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; font-weight:bold;'>3. Infusões Vasoativas (mcg/kg/min)</p>", unsafe_allow_html=True)
    # Espaço com autocomplete: o utilizador escreve a droga (os principais medicamentos sugeridos)
    if 'vasoativos' not in st.session_state:
        st.session_state.vasoativos = []
    droga_vaso = st.text_input("Droga (ex.: adrenalina, noradrenalina, dopamina, dobutamina, milrinona, aminofilina)", key="droga_vaso")
    dose_vaso = st.number_input("Dose (mcg/kg/min)", min_value=0.0, step=0.1, key="dose_vaso")
    if st.button("Adicionar Vasoativo", key="add_vaso"):
        if droga_vaso:
            st.session_state.vasoativos.append((droga_vaso, dose_vaso))
    if st.session_state.vasoativos:
        st.markdown("**Vasoativos adicionados:**")
        for item in st.session_state.vasoativos:
            st.write(f"{item[0]}: {item[1]} mcg/kg/min")
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Seção 4: Avaliação Neurológica - Glasgow Coma Scale (3-15)
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; font-weight:bold;'>4. Avaliação Neurológica - Glasgow Coma Scale (3-15)</p>", unsafe_allow_html=True)
    gcs = st.slider("GCS", min_value=3, max_value=15, value=15)
    avpu = st.radio("Nível AVPU", options=["Alert", "Verbal", "Pain", "Unresponsive"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Seção 5: Avaliação de Sedação e Analgesia em Perfusão
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("5. Avaliação de Sedação e Analgesia em Perfusão")
    if 'sedacao' not in st.session_state:
        st.session_state.sedacao = []
    droga_sed = st.text_input("Droga (ex.: morfina, fentanil, midazol, cetamina, propofol, dexmedetomidina, rocurônio)", key="droga_sed")
    dose_sed = st.number_input("Dose (mg/kg/h ou mcg/kg/h)", min_value=0.0, step=0.1, key="dose_sed")
    if st.button("Adicionar Droga Sedação", key="add_sed"):
        if droga_sed:
            st.session_state.sedacao.append((droga_sed, dose_sed))
    if st.session_state.sedacao:
        st.markdown("**Drogas de sedação adicionadas:**")
        for droga in st.session_state.sedacao:
            st.write(f"{droga[0]}: {droga[1]}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Seção 6: Suporte Avançado e Complicações + Características do trajeto
    ##############################
    st.markdown("<div style='border:3px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("6. Suporte Avançado e Complicações")
    drenagem_toracica = st.radio("Drenagem torácica", options=["Sim", "Não"])
    drenagem_vesical = st.radio("Drenagem vesical", options=["Sim", "Não"])
    crrt = st.radio("Terapia renal contínua (CRRT)", options=["Sim", "Não"])
    arritmias = st.radio("Arritmias inestáveis nas últimas 3h", options=["Sim", "Não"])
    hipertensao_intracranica = st.radio("Sospeita de hipertensão intracraniana aguda", options=["Sim", "Não"])
    st.markdown("**Características do trajeto:**")
    trajeto_andar = st.radio("O transporte é no mesmo andar?", options=["Sim", "Não"])
    elevador = st.radio("Necessita utilizar elevador?", options=["Sim", "Não"])
    space_elevador = "Não Aplicável"
    if elevador == "Sim":
        space_elevador = st.radio("O elevador tem espaço suficiente para cama e ventilador?", options=["Sim", "Não"])
    tempo_transporte = st.number_input("Tempo de transporte (minutos)", min_value=0, step=1)
    st.markdown("</div>", unsafe_allow_html=True)
    
    ##############################
    # Botão final – Calcular risco de transporte e mostrar modal
    ##############################
    if st.button("Calcular risco de transporte", key="calc_risco"):
        # Função para calcular o score (exemplo simplificado)
        def calcular_risco():
            score = 0
            # Avaliação Respiratória
            if fio2 > 80:
                score += 5
            elif fio2 > 60:
                score += 3
            elif fio2 > 50:
                score += 2
            elif fio2 > 40:
                score += 1
            
            # Modalidade ventilatória:
            if modalidade == "Ventilação Mecânica Invasiva (VMI)":
                try:
                    valor = float(nivel_tubo) if nivel_tubo.strip() != "" else 0
                    if valor >= 8:
                        score += 2
                except:
                    pass
                if fixacao == "Não":
                    score += 2
                if auscultacao == "Não":
                    score += 2
            elif modalidade == "Ventilação Não Invasiva (VNI)":
                if protecao_facial == "Não":
                    score += 1
                if resp_dif_vni == "Sim":
                    score += 2
            elif modalidade == "Oxigenoterapia de Alto Fluxo (OAF)":
                if fluxos == "Não":
                    score += 2
                if resp_dif_oaf == "Sim":
                    score += 2
            elif modalidade == "Oxigênio Suplementar":
                if tipo_mascara == "Máscara de Venturi":
                    score += 2
                else:
                    score += 1
                if resp_dif_sup == "Sim":
                    score += 2
            
            # Avaliação Hemodinâmica:
            if pas < 60:
                score += 2
            if pad < 40:
                score += 1
            if pam < 50:
                score += 2
            if satO2 < 90:
                score += 2
            
            # Infusões Vasoativas:
            total_vaso = sum([dose for _, dose in st.session_state.vasoativos]) if st.session_state.vasoativos else 0
            if total_vaso > 20:
                score += 