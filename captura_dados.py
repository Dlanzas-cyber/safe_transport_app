import streamlit as st
from datetime import datetime
from fpdf import FPDF
import io

# ----------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------
st.set_page_config(page_title="Avaliação Transporte Pediátrico", layout="wide")

# Criação das abas
abas = st.tabs(["Passo 1: Dados do doente", "Passo 2 – Avaliação do risco de transporte"])

# ----------------------------
# PASSO 1: Dados do doente
# ----------------------------
with abas[0]:
    st.title("Passo 1: Dados do doente")
    st.markdown("Insira os dados básicos do doente e do transporte.")

    with st.expander("Dados do doente", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_utente = st.text_input("Nome do utente *")
            idade = st.number_input("Idade", min_value=0, step=1)
            unidade_idade = st.selectbox("Unidade de idade", options=["Dias", "Meses", "Anos"], index=2)
            peso = st.number_input("Peso (kg) *", min_value=0.0, step=0.1, format="%.1f")
        with col2:
            diagnosticos = [
                "Pneumonia", "Choque séptico", "Insuficiência respiratória aguda",
                "Estado convulsivo", "Cardiopatia congénita", "Traumatismo craniano",
                "Bronquiolite", "Asma", "Sepse neonatal"
            ]
            opcoes_diagnostico = diagnosticos + ["Outro (escrever)"]
            diagnostico_selecionado = st.selectbox("Diagnóstico principal", options=opcoes_diagnostico)
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

# ----------------------------
# PASSO 2 – Avaliação do risco
# ----------------------------
with abas[1]:
    # [restante do código permanece quase idêntico]
    # A única alteração relevante aqui é substituir o uso de `st.modal()` por uma exibição condicional:

    if st.button("Calcular risco de transporte", key="calc_risco"):
        risco_final = calcular_risco()  # usar sua função aqui
        explicacao = {
            1: "Transporte seguro.",
            2: "Transporte viável com monitorização reforçada.",
            3: "Transporte com precauções avançadas.",
            4: "Transporte de alto risco – requer equipa especializada.",
            5: "Transporte contraindicado – reavaliar o estado clínico."
        }[risco_final]

        st.markdown("---")
        st.subheader(f"🟠 Resultado da Avaliação de Risco: Nível {risco_final}")
        st.info(explicacao)

        if st.button("Gerar Relatório PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Relatório de Avaliação do Risco de Transporte", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Risco: {risco_final} - {explicacao}", ln=True, align='L')
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("📄 Descarregar Relatório PDF", data=pdf_output,
                               file_name="relatorio_transporte.pdf", mime="application/pdf")

