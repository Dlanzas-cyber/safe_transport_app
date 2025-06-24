import streamlit as st
from datetime import datetime

#####################
# CONFIGURAÇÃO DA PÁGINA
#####################
st.set_page_config(page_title="Avaliação Transporte Pediátrico", layout="wide")

# Criação das abas
abas = st.tabs(["Dados do doente", "Árvore de Decisão – Risco de Transporte"])

####################################
# ABA 1: Dados do doente
####################################
with abas[0]:
    st.title("Módulo 1: Dados do doente")
    st.markdown("Insira os dados básicos do doente e do transporte.")
    
    with st.expander("Dados do doente", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_utente = st.text_input("Nome do utente *")
            # Idade: número inteiro sem decimais.
            idade = st.number_input("Idade", min_value=0, step=1)
            # A unidade de idade vem depois da idade.
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
    
    if st.button("Submeter Dados do Doente"):
        st.success("Dados do doente submetidos com sucesso!")
        st.markdown("### Resumo:")
        st.write(f"**Nome:** {nome_utente}")
        st.write(f"**Idade:** {idade} {unidade_idade}")
        st.write(f"**Peso:** {peso} kg")
        st.write(f"**Diagnóstico:** {diagnostico_final}")
        st.write(f"**Data do Transporte:** {data_transporte.strftime('%d/%m/%Y')}")
        st.write(f"**Hora do Transporte:** {hora_transporte.strftime('%H:%M')}")

####################################
# ABA 2: Árvore de Decisão – Risco de Transporte
####################################
with abas[1]:
    st.title("Módulo 2: Árvore de Decisão – Risco de Transporte")
    st.markdown("Preencha os parâmetros (médias das últimas 3 horas) para avaliar o risco do transporte:")

    #####################
    # Seção 1: Avaliação Respiratória (com árvore de decisão)
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("1. Avaliação Respiratória")
    
    # Perguntar a modalidade ventilatória com árvore de decisão:
    modalidade = st.selectbox("Modalidade ventilatória", 
              options=[
                  "Ventilação Mecânica Invasiva (VMI)", 
                  "Ventilação Não Invasiva (VNI)", 
                  "Oxigenoterapia de Alto Fluxo (OAF)", 
                  "Oxigênio Suplementar", 
                  "Ar ambiente"
              ])
    
    # Condicionais conforme a opção:
    if modalidade == "Ventilação Mecânica Invasiva (VMI)":
        tube_level = st.selectbox("Nível do tubo Oro-traqueal", options=["Baixo", "Médio", "Alto"])
        fixacao = st.radio("Fixação do tubo adequada", options=["Sim", "Não"])
        ausc = st.radio("Auscultação simétrica", options=["Sim", "Não"])
    elif modalidade == "Ventilação Não Invasiva (VNI)":
        vni_mod = st.selectbox("Modalidade", options=["CPAP", "BIPAP"])
        facial = st.radio("Placas de proteção facial", options=["Sim", "Não"])
        resp_dif_vni = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    elif modalidade == "Oxigenoterapia de Alto Fluxo (OAF)":
        fluxos = st.radio("Fluxos estão adequados", options=["Sim", "Não"])
        resp_dif_oaf = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    elif modalidade == "Oxigênio Suplementar":
        mascara = st.selectbox("Tipo de máscara", options=["Máscara de alto débito", "Máscara de Venturi", "Máscara simples", "O2 por óculos nasais"])
        resp_dif_sup = st.radio("Sinais de dificuldade respiratória", options=["Sim", "Não"])
    # "Ar ambiente": nenhuma pergunta adicional.
    fiO2 = st.number_input("FiO₂ média das últimas 3h (%)", min_value=21, max_value=100, value=21)
    st.markdown("</div>", unsafe_allow_html=True)

    #####################
    # Seção 2: Avaliação Hemodinâmica
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("2. Avaliação Hemodinâmica")
    fc = st.number_input("Frequência cardíaca média (lpm)", min_value=0, step=1)
    pas = st.number_input("Pressão arterial sistólica (mmHg)", min_value=0, step=1)
    pad = st.number_input("Pressão arterial diastólica (mmHg)", min_value=0, step=1)
    pam = st.number_input("Pressão arterial média (mmHg)", min_value=0, step=1)
    st.markdown("</div>", unsafe_allow_html=True)
    
    #####################
    # Seção 3: Infusões Vasoativas (com autocomplete)
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("3. Infusões Vasoativas (mcg/kg/min)")
    # Aumentar o tamanho das letras nas labels usando HTML inline:
    st.markdown("<p style='font-size:18px;'><b>Infusões:</b></p>", unsafe_allow_html=True)
    if 'vasoativos' not in st.session_state:
        st.session_state.vasoativos = []
    vasoativo_droga = st.text_input("Droga", key="droga_vasoativo")
    vasoativo_dose = st.number_input("Dose (mcg/kg/min)", min_value=0.0, step=0.1, key="dose_vasoativo")
    if st.button("Adicionar Vasoativo", key="add_vasoativo"):
        if vasoativo_droga and vasoativo_dose is not None:
            st.session_state.vasoativos.append((vasoativo_droga, vasoativo_dose))
    if st.session_state.vasoativos:
        st.markdown("**Vasoativos adicionados:**")
        for item in st.session_state.vasoativos:
            st.write(f"{item[0]}: {item[1]} mcg/kg/min")
    st.markdown("</div>", unsafe_allow_html=True)
    
    #####################
    # Seção 4: Avaliação Neurológica
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px; font-weight:bold;'>4. Avaliação Neurológica - Glasgow Coma Scale (3-15)</span>", unsafe_allow_html=True)
    gcs = st.slider("GCS", min_value=3, max_value=15, value=15)
    avpu = st.radio("Nível AVPU", options=["Alert", "Verbal", "Pain", "Unresponsive"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    #####################
    # Seção 5: Avaliação de Sedação e Analgesia em Perfusão (com autocomplete)
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("5. Avaliação de Sedação e Analgesia em Perfusão")
    if 'sedacao' not in st.session_state:
        st.session_state.sedacao = []
    sedacao_droga = st.text_input("Droga", key="droga_sedacao")
    if st.button("Adicionar Droga", key="add_sedacao"):
        if sedacao_droga:
            st.session_state.sedacao.append(sedacao_droga)
    if st.session_state.sedacao:
        st.markdown("**Drogas adicionadas:**")
        for droga in st.session_state.sedacao:
            st.write(droga)
    st.markdown("</div>", unsafe_allow_html=True)
    
    #####################
    # Seção 6: Suporte Avançado e Complicações + Características do trajeto
    #####################
    st.markdown("<div style='border:2px solid #000; padding:10px; margin-bottom:10px;'>", unsafe_allow_html=True)
    st.subheader("6. Suporte Avançado e Complicações")
    drenagem_toracica = st.radio("Drenagem torácica", options=["Sim", "Não"])
    drenagem_vesical = st.radio("Drenagem vesical", options=["Sim", "Não"])
    crrt = st.radio("Terapia renal contínua (CRRT)", options=["Sim", "Não"])
    arritmias = st.radio("Arritmias inestáveis nas últimas 3h", options=["Sim", "Não"])
    hipertensao = st.radio("Sospeita de hipertensão intracraniana aguda", options=["Sim", "Não"])
    st.markdown("**Características do trajeto:**")
    trajeto_andar = st.radio("O transporte é no mesmo andar?", options=["Sim", "Não"])
    elevador = st.radio("Necessita utilizar elevador?", options=["Sim", "Não"])
    space_elevador = "Não Aplicável"
    if elevador == "Sim":
        space_elevador = st.radio("O elevador tem espaço suficiente para cama e ventilador?", options=["Sim", "Não"])
    tempo_transporte = st.number_input("Tempo de transporte (minutos)", min_value=0, step=1)
    st.markdown("</div>", unsafe_allow_html=True)
    
    #####################
    # Botão final – Submeter Avaliação e exibir pop-up com o risco
    #####################
    if st.button("Submeter Avaliação"):
        # Função dummy para cálculo de risco
        def calcular_risco():
            score = 0
            # Avaliação Respiratória
            if fiO2 > 80:
                score += 5
            elif fiO2 > 60:
                score += 3
            elif fiO2 > 50:
                score += 2
            elif fiO2 > 40:
                score += 1
            # Sinais de dificuldade respiratória (baseado na modalidade)
            if modalidade == "Ventilação Mecânica Invasiva (VMI)":
                if tube_level == "Alto":
                    score += 2
                if fixacao == "Não":
                    score += 2
                if ausc == "Não":
                    score += 2
            elif modalidade == "Ventilação Não Invasiva (VNI)":
                if facial == "Não":
                    score += 1
                if resp_dif_vni == "Sim":
                    score += 2
            elif modalidade == "Oxigenoterapia de Alto Fluxo (OAF)":
                if fluxos == "Não":
                    score += 2
                if resp_dif_oaf == "Sim":
                    score += 2
            elif modalidade == "Oxigênio Suplementar":
                if mascara == "Máscara de Venturi":
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
            
            # Infusões vasoativas:
            total_vaso = sum([dose for _, dose in st.session_state.vasoativos])
            if total_vaso > 20:
                score += 5
            elif total_vaso > 10:
                score += 3
            elif total_vaso > 0:
                score += 1
            
            # Avaliação Neurológica:
            if gcs < 8:
                score += 5
            elif gcs < 10:
                score += 3
            elif gcs < 13:
                score += 2
            
            # Sedação/Analgesia:
            if st.session_state.sedacao:
                score += len(st.session_state.sedacao)
            
            # Suporte Avançado e Complicações:
            if drenagem_toracica == "Sim":
                score += 2
            if drenagem_vesical == "Sim":
                score += 1
            if crrt == "Sim":
                score += 2
            if arritmias == "Sim":
                score += 2
            if hipertensao == "Sim":
                score += 2
            if elevador == "Sim" and space_elevador == "Não":
                score += 2
            if tempo_transporte > 20:
                score += 2
            
            return score
        
        risk_score = calcular_risco()
        # Mapeamento do score para nível de risco:
        if risk_score >= 20:
            risco_final = 5
        elif risk_score >= 16:
            risco_final = 4
        elif risk_score >= 12:
            risco_final = 3
        elif risk_score >= 8:
            risco_final = 2
        else:
            risco_final = 1
        
        # Pop-up simulado com um retângulo:
        st.markdown("<div style='border:3px solid #000; padding:15px; margin-top:20px;'>", unsafe_allow_html=True)
        st.markdown(f"<h2>Risco de Transporte: {risco_final}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
