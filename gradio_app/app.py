"""Cadastro de Pacientes — versão Gradio (execução local).

Grava cada cadastro como uma nova linha em pacientes.csv (mesma pasta deste
arquivo) e mostra os últimos pacientes cadastrados.

Executar:  python app.py   ->  abre em http://127.0.0.1:7860
"""

import os
from datetime import datetime

import gradio as gr
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")

COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def ultimos_pacientes(n=5):
    """Lê o CSV e devolve as últimas n linhas (ou uma tabela vazia)."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV, encoding="utf-8").tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    nome = (nome or "").strip()
    motivo = (motivo or "").strip()

    # Validação simples antes de gravar
    if not nome:
        return "⚠️ Informe o nome do paciente.", ultimos_pacientes()
    if idade is None or not 0 <= idade <= 120:
        return "⚠️ Informe uma idade entre 0 e 120.", ultimos_pacientes()
    if not convenio:
        return "⚠️ Selecione o convênio.", ultimos_pacientes()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    # Cria o arquivo com cabeçalho na primeira vez; depois só acrescenta linhas
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8")
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False, encoding="utf-8")

    return f"✅ Paciente {nome} cadastrado com sucesso!", ultimos_pacientes()


# Layout em coluna única para funcionar bem no celular
with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes\nPreencha os dados e clique em **Cadastrar**.")

    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = gr.Number(label="Idade", minimum=0, maximum=120, precision=0)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value="Particular")
    prioridade = gr.Slider(1, 5, step=1, value=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        lines=3,
        placeholder="Ex.: dor de cabeça há 3 dias",
    )

    botao = gr.Button("Cadastrar", variant="primary")

    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", interactive=False)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

    # Mostra os registros já existentes ao abrir a página
    demo.load(ultimos_pacientes, None, tabela)


if __name__ == "__main__":
    demo.launch()
