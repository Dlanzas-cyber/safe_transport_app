import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Avaliação Transporte Pediátrico", layout="wide")

# Criação das abas
abas = st.tabs(["Dados do doente", "Árvore de Decisão"])

# --------------------- Aba 1: Dados do doente ---------------------
with abas[0]:
    st.title("Módulo 1: Dados do doente")
    st.markdown("Insira os dados básicos do doente e do transporte.")
    
    with st.expander("Dados do doente", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_utente = st.text_input("Nome do utente *")
            # Idade como número inteiro (sem decimais)
            idade = st.number_input("Idade", min_value=0, step=1)
            # Unidade de idade (após a idade)
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
        st.markdown("### Resumo dos Dados:")
        st.write(f"**Nome:** {nome_utente}")
        st.write(f"**Idade:** {idade} {unidade_idade}")
        st.write(f"**Peso:** {peso} kg")
        st.write(f"**Diagnóstico:** {diagnostico_final}")
        st.write(f"**Data do Transporte:** {data_transporte.strftime('%d/%m/%Y')}")
        st.write(f"**Hora do Transporte:** {hora_transporte.strftime('%H:%M')}")

# --------------------- Aba 2: Árvore de Decisão ---------------------
with abas[1]:
    st.title("Módulo 2: Árvore de Decisão - Risco de Transporte")
    st.markdown("Preencha os parâmetros (médias das últimas 3 horas) para avaliar o risco do transporte:")

    # 1. Avaliação Respiratória
    st.subheader("1. Avaliação Respiratória")
    col_resp1, col_resp2, col_resp3 = st.columns(3)
    fio2 = col_resp1.slider("FiO₂ média (%)", min_value=21, max_value=100, value=21)
    peep = col_resp2.number_input("PEEP média (cmH₂O)", min_value=0.0, step=0.5)
    spo2 = col_resp3.number_input("SpO₂ média (%)", min_value=50, max_value=100, step=1)
    modo_vent = st.radio("Modalidade ventilatória", options=[
        "Ventilação mecânica invasiva", "CPAP/NIV", "Oxigenoterapia de alto fluxo", "Espontâneo com cânula"
    ])

    # 2. Avaliação Hemodinâmica
    st.subheader("2. Avaliação Hemodinâmica")
    col_hemo1, col_hemo2, col_hemo3 = st.columns(3)
    fc = col_hemo1.number_input("Frequência cardíaca média (lpm)", min_value=0, step=1)
    pas = col_hemo2.number_input("Pressão arterial sistólica (mmHg)", min_value=0, step=1)
    # Usaremos somente a pressão sistólica para simplificar.
    
    st.markdown("**Infusões vasoativas (mcg/kg/min):**")
    col_vaso1, col_vaso2, col_vaso3 = st.columns(3)
    dopamina = col_vaso1.number_input("Dopamina", min_value=0.0, step=0.1)
    dobutamina = col_vaso1.number_input("Dobutamina", min_value=0.0, step=0.1)
    norad = col_vaso2.number_input("Noradrenalina", min_value=0.0, step=0.01)
    adren = col_vaso2.number_input("Adrenalina", min_value=0.0, step=0.01)
    milrinona = col_vaso3.number_input("Milrinona", min_value=0.0, step=0.01)
    outras = col_vaso3.text_input("Outras (mcg/kg/min, se houver)", value="0")
    try:
        outras_val = float(outras)
    except:
        outras_val = 0.0

    # 3. Avaliação Neurológica
    st.subheader("3. Avaliação Neurológica")
    gcs = st.slider("Glasgow Coma Scale (3-15)", min_value=3, max_value=15, value=15)
    avpu = st.radio("Nível AVPU", options=["Alert", "Verbal", "Pain", "Unresponsive"])

    # 4. Avaliação de Sedação e Analgesia
    st.subheader("4. Avaliação de Sedação e Analgesia")
    intubacao = st.radio("Entubação Oro-traqueal", options=["Sim", "Não"])
    fixacao = st.radio("Fixação do tubo adequada", options=["Sim", "Não"])
    comfort = st.number_input("COMFORT–B (6-30)", min_value=6, max_value=30, step=1)

    # 5. Suporte Avançado e Complicações
    st.subheader("5. Suporte Avançado e Complicações")
    drenagem_toracica = st.radio("Drenagem torácica", options=["Sim", "Não"])
    drenagem_vesical = st.radio("Drenagem vesical", options=["Sim", "Não"])
    crrt = st.radio("Terapia renal contínua (CRRT)", options=["Sim", "Não"])
    arritmias = st.radio("Arritmias inestáveis nas últimas 3h", options=["Sim", "Não"])
    hipertensao_intracranica = st.radio("Sospeita de hipertensão intracraniana aguda", options=["Sim", "Não"])

    # Função para calcular o Vasoactive-Inotropic Score (VIS)
    def calcular_vis(dopamina, dobutamina, norad, adren, milrinona, outras):
        return dopamina + dobutamina + 100 * (norad + adren) + 10 * (milrinona + outras)

    # Função de decisão: árvore de decisão para o risco de transporte
    def calcular_risco(fio2, peep, spo2, gcs, avpu, vis, arritmias, hipertensao):
        # Risco 5: Crítico/contraindicado
        if (fio2 > 80 or peep > 10 or spo2 < 85 or vis > 20 or gcs < 8 or avpu == "Unresponsive"
            or arritmias == "Sim" or hipertensao == "Sim"):
            return 5
        # Risco 4: Elevado
        elif (fio2 > 60 or peep > 8 or spo2 < 90 or vis > 10 or gcs < 10):
            return 4
        # Risco 3: Moderado
        elif (fio2 > 50 or peep > 5 or spo2 < 92 or vis > 5 or gcs < 13):
            return 3
        # Risco 2: Leve
        elif (fio2 > 40):
            return 2
        else:
            return 1

    if st.button("📊 Calcular Risco de Transporte"):
        vis = calcular_vis(dopamina, dobutamina, norad, adren, milrinona, outras_val)
        risco = calcular_risco(fio2, peep, spo2, gcs, avpu, vis, arritmias, hipertensao_intracranica)
        st.subheader("Resultado da Avaliação:")
        if risco == 1:
            st.success("Risco 1: Transporte seguro.")
        elif risco == 2:
            st.info("Risco 2: Transporte viável com monitorização reforçada.")
        elif risco == 3:
            st.warning("Risco 3: Transporte com precauções avançadas.")
        elif risco == 4:
            st.error("Risco 4: Transporte de alto risco – requer equipa especializada.")
        elif risco == 5:
            st.error("Risco 5: Transporte contraindicado – reavaliar o estado clínico.")
