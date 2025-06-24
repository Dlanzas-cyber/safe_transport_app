import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Captura de Dados - Módulo 1", layout="wide")

# Cria uma pestana chamada "Dados do doente"
abas = st.tabs(["Dados do doente"])

with abas[0]:
    st.title("Captura de Dados - Módulo 1: Dados do doente")
    st.markdown("**Insira os dados básicos do doente e do transporte.**")
    
    with st.expander("Dados do doente", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Nome, idade (com unidade) e peso do utente
            nome_utente = st.text_input("Nome do utente *")
            # Seleção da unidade para a idade: Dias, Meses ou Anos
            unidade_idade = st.selectbox("Unidade de idade", options=["Dias", "Meses", "Anos"], index=2)
            idade = st.number_input("Idade", min_value=0.0, step=0.1, format="%.1f")
            peso = st.number_input("Peso (kg) *", min_value=0.0, format="%.1f")
        
        with col2:
            # Diagnóstico com autocompletar: se não estiver na lista, permite inserção manual
            diagnosticos = [
                "Pneumonia", "Choque séptico", "Insuficiência respiratória aguda",
                "Estado convulsivo", "Cardiopatia congénita",
                "Traumatismo craniano", "Bronquiolite", "Asma", "Sepse neonatal"
            ]
            opcoes_diagnostico = diagnosticos + ["Outro (escrever)"]
            diagnostico_selecionado = st.selectbox("Diagnóstico principal (autocompletar)", options=opcoes_diagnostico)
            if diagnostico_selecionado == "Outro (escrever)":
                diagnostico_final = st.text_input("Introduza o diagnóstico manualmente")
            else:
                diagnostico_final = diagnostico_selecionado
                
            # Data e hora do transporte
            data_transporte = st.date_input("Data do transporte *", value=datetime.now().date())
            hora_transporte = st.time_input("Hora do transporte *", value=datetime.now().time())
    
    # Botão que submete os dados e exibe um resumo
    if st.button("Submeter Dados"):
        st.success("Dados submetidos com sucesso!")
        st.markdown("### Resumo dos Dados:")
        st.write(f"**Nome:** {nome_utente}")
        st.write(f"**Idade:** {idade} {unidade_idade}")
        st.write(f"**Peso:** {peso} kg")
        st.write(f"**Diagnóstico:** {diagnostico_final}")
        st.write(f"**Data do Transporte:** {data_transporte.strftime('%d/%m/%Y')}")
        st.write(f"**Hora do Transporte:** {hora_transporte.strftime('%H:%M')}")
