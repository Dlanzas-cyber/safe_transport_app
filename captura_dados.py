import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Captura de Dados - Módulo 1", layout="wide")
st.title("Captura de Dados - Módulo 1")
st.markdown("**Insira os dados básicos do utente e do transporte.**")

# Módulo de Identificação do Utente
with st.expander("1. Identificação do Utente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nome_utente = st.text_input("Nome do Utente *")
        idade = st.number_input("Idade (anos) *", min_value=0.0, format="%.1f")
        peso = st.number_input("Peso (kg) *", min_value=0.0, format="%.1f")
    with col2:
        # Diagnóstico principal com autocomplete
        diagnosticos = [
            "Pneumonia", "Choque séptico", "Insuficiência respiratória aguda",
            "Estado convulsivo", "Cardiopatia congénita", "Traumatismo craniano",
            "Bronquiolite", "Asma", "Sepse neonatal", "Outro"
        ]
        diagnostico_principal = st.selectbox("Diagnóstico Principal *", options=diagnosticos)
        if diagnostico_principal == "Outro":
            diagnostico_principal = st.text_input("Por favor, especifique o diagnóstico")
        # Data e Hora do Transporte
        data_transporte = st.date_input("Data do Transporte *", value=datetime.now().date())
        hora_transporte = st.time_input("Hora do Transporte *", value=datetime.now().time())

# Botão para submeter os dados
if st.button("Submeter Dados"):
    st.success("Dados submetidos com sucesso!")
    st.markdown("### Resumo da Captura de Dados:")
    st.write(f"**Nome:** {nome_utente}")
    st.write(f"**Idade:** {idade} anos")
    st.write(f"**Peso:** {peso} kg")
    st.write(f"**Diagnóstico Principal:** {diagnostico_principal}")
    st.write(f"**Data do Transporte:** {data_transporte.strftime('%d/%m/%Y')}")
    st.write(f"**Hora do Transporte:** {hora_transporte.strftime('%H:%M')}")
