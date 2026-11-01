"""Cadastro de Pacientes — versão Streamlit (deploy no Streamlit Community Cloud).

Os pacientes ficam em st.session_state durante a sessão e também são gravados
em pacientes.csv. Como o disco do Community Cloud é efêmero, o botão
"Baixar CSV" permite exportar os dados da sessão.

Executar localmente:  streamlit run app.py
"""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]

st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")
st.title("🏥 Cadastro de Pacientes")
st.caption("Preencha os dados do paciente e clique em **Cadastrar**.")

# Pacientes cadastrados nesta sessão
if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS)
    prioridade = st.slider("Prioridade do atendimento (5 = urgente)", 1, 5)
    motivo = st.text_area("Motivo da consulta / observações", placeholder="Ex.: dor de cabeça há 3 dias")
    enviado = st.form_submit_button("Cadastrar", type="primary", width="stretch")

if enviado:
    if not nome.strip():
        st.error("⚠️ Informe o nome do paciente.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        novo = pd.DataFrame([nova_linha], columns=COLUNAS)

        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, novo], ignore_index=True
        )

        # Mesma lógica de gravação da versão Gradio (arquivo efêmero na nuvem)
        try:
            novo.to_csv(
                ARQUIVO_CSV,
                mode="a",
                header=not os.path.exists(ARQUIVO_CSV),
                index=False,
                encoding="utf-8",
            )
        except OSError as erro:
            st.warning(f"Não foi possível gravar o arquivo local: {erro}")

        st.success(f"✅ Paciente {nova_linha['nome']} cadastrado!")

st.subheader("Últimos pacientes cadastrados")
if st.session_state.pacientes.empty:
    st.info("Nenhum paciente cadastrado nesta sessão.")
else:
    st.dataframe(st.session_state.pacientes.tail(5), hide_index=True)

csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar CSV",
    csv,
    "pacientes.csv",
    "text/csv",
    disabled=st.session_state.pacientes.empty,
    width="stretch",
)
