import streamlit as st
from datetime import datetime
from fpdf import FPDF
import os
import urllib.request

# --- Setup Fonte UTF-8 para PDF ---
FONT_FILE = "DejaVuSans.ttf"
FONT_URL = "https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans.ttf?raw=true"
if not os.path.exists(FONT_FILE):
    urllib.request.urlretrieve(FONT_URL, FONT_FILE)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", FONT_FILE, uni=True)
        self.set_font("DejaVu", "", 12)
        self.add_page()

    def add_title(self, title):
        self.set_font("DejaVu", "", 16)
        self.cell(0, 10, txt=title, ln=True, align="C")
        self.ln(10)
        self.set_font("DejaVu", "", 12)

    def add_line(self, label, value):
        self.cell(0, 10, txt=f"{label}: {value}", ln=True)

# --- Página Streamlit ---
st.set_page_config("Avaliação Transporte Pediátrico", layout="wide")
abas = st.tabs(["Passo 1: Dados do doente", "Passo 2 – Avaliação do risco de transporte"])

# --------------------------------------
# PASSO 1 – DADOS DO DOENTE
# --------------------------------------
with abas[0]:
    st.title("Passo 1: Dados do doente")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do utente *")
        idade = st.number_input("Idade", min_value=0, step=1)
        unidade_idade = st.selectbox("Unidade", ["Dias", "Meses", "Anos"])
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
    with col2:
        diagnostico_opcoes = ["Pneumonia", "Sepse", "Bronquiolite", "Outro (especificar)"]
        diagnostico = st.selectbox("Diagnóstico", diagnostico_opcoes)
        if diagnostico == "Outro (especificar)":
            diagnostico = st.text_input("Diagnóstico manual")
        data_transporte = st.date_input("Data", value=datetime.now().date())
        hora_transporte = st.time_input("Hora", value=datetime.now().time())

# --------------------------------------
# PASSO 2 – RISCO + RELATÓRIO
# --------------------------------------
with abas[1]:
    st.title("Passo 2 – Avaliação do risco de transporte")
    fio2 = st.number_input("FiO₂ média das últimas 3 h (%)", min_value=21, max_value=100, value=21)
    pas = st.number_input("Pressão arterial sistólica", min_value=0)
    pam = st.number_input("Pressão arterial média", min_value=0)
    satO2 = st.number_input("SatO₂ (%)", min_value=0, max_value=100)
    gcs = st.slider("Glasgow Coma Scale", 3, 15, 15)
    tempo_transporte = st.number_input("Tempo de transporte (minutos)", min_value=0)

    if st.button("Calcular risco de transporte"):
        score = 0
        if fio2 > 80: score += 5
        elif fio2 > 60: score += 3
        elif fio2 > 40: score += 1
        if pas < 60: score += 2
        if pam < 50: score += 2
        if satO2 < 90: score += 2
        if gcs < 8: score += 5
        elif gcs < 13: score += 3
        if tempo_transporte > 20: score += 2

        if score >= 20: nivel = 5
        elif score >= 16: nivel = 4
        elif score >= 12: nivel = 3
        elif score >= 8: nivel = 2
        else: nivel = 1

        explicacao = {
            1: "Transporte seguro.",
            2: "Viável com monitorização reforçada.",
            3: "Precauções avançadas necessárias.",
            4: "Alto risco – requer equipa especializada.",
            5: "Contraindicado – reavaliar estado clínico."
        }[nivel]

        st.markdown(f"### 🩺 Nível de Risco: **{nivel}**")
        st.info(explicacao)

        # --- Geração do PDF ---
        pdf = PDF()
        pdf.add_title("Relatório de Avaliação do Transporte Pediátrico")
        pdf.add_line("Nome", nome)
        pdf.add_line("Idade", f"{idade} {unidade_idade}")
        pdf.add_line("Peso", f"{peso} kg")
        pdf.add_line("Diagnóstico", diagnostico)
        pdf.add_line("Data", data_transporte.strftime('%d/%m/%Y'))
        pdf.add_line("Hora", hora_transporte.strftime('%H:%M'))
        pdf.ln(5)
        pdf.add_line("FiO₂", f"{fio2}%")
        pdf.add_line("PAS", f"{pas} mmHg")
        pdf.add_line("PAM", f"{pam} mmHg")
        pdf.add_line("SatO₂", f"{satO2}%")
        pdf.add_line("GCS", str(gcs))
        pdf.add_line("Tempo transporte", f"{tempo_transporte} min")
        pdf.ln(5)
        pdf.add_line("Risco final", f"{nivel} – {explicacao}")

        st.download_button("📄 Descarregar PDF", pdf.output(dest="S").encode("utf-8"),
                           file_name="relatorio_transporte.pdf", mime="application/pdf")
