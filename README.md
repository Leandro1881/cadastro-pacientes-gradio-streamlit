# Cadastro de Pacientes — Gradio x Streamlit

A mesma aplicação de coleta de dados feita duas vezes, para comparar as duas bibliotecas.
É um cadastro de pacientes para a recepção de um consultório. Campos: nome, idade, convênio, prioridade (1 a 5) e motivo da consulta. Cada envio grava uma linha com data/hora.

```
gradio_app/
├── app.py            # versão Gradio (roda local, grava gradio_app/pacientes.csv)
└── pacientes.csv     # exemplo gerado nos testes
streamlit_app/
├── app.py            # versão Streamlit (publicada no Streamlit Community Cloud)
└── requirements.txt
requirements.txt
```

## Instalar

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# Linux/macOS:  source .venv/bin/activate
pip install -r requirements.txt
```

## Parte 1 — Gradio (local)

```bash
python gradio_app/app.py
```

Abra `http://127.0.0.1:7860`. O layout usa uma coluna única para funcionar bem no celular.
Cada clique em **Cadastrar** grava uma linha em `gradio_app/pacientes.csv`. O arquivo é criado com cabeçalho na primeira vez.
A tela mostra uma mensagem de confirmação e os 5 últimos pacientes.

## Parte 2 — Streamlit (nuvem)

Rodar localmente:

```bash
streamlit run streamlit_app/app.py
```

- O formulário usa `st.form(clear_on_submit=True)`.
- Os pacientes da sessão ficam em `st.session_state.pacientes`.
- O app também grava em `streamlit_app/pacientes.csv`. No Community Cloud esse disco é efêmero: o arquivo some quando o app reinicia. Por isso há o botão **Baixar CSV** (`st.download_button`), que exporta os pacientes da sessão.

### Deploy no Streamlit Community Cloud

1. Crie um repositório **público** no GitHub e envie esta pasta:
   ```bash
   git init
   git add .
   git commit -m "Cadastro de pacientes: Gradio e Streamlit"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/cadastro-pacientes.git
   git push -u origin main
   ```
2. Acesse [share.streamlit.io](https://share.streamlit.io) e entre com a conta do GitHub.
3. Clique em **New app**. Escolha o repositório, a branch `main` e o arquivo `streamlit_app/app.py`.
4. Aguarde o build. Teste pelo link público (`https://<nome>.streamlit.app`).
5. Abra o mesmo link no celular e teste o formulário.

## Comparação rápida

| | Gradio | Streamlit |
|---|---|---|
| Modelo | Eventos: cada botão chama uma função | Script reexecutado de cima a baixo a cada interação |
| Estado | Valores dos componentes / `gr.State` | `st.session_state` |
| Formulário | Componentes soltos + `button.click` | `st.form` agrupa e envia tudo de uma vez |
| Link público | `share=True` (temporário, 1 semana) | Community Cloud (permanente, ligado ao GitHub) |
| Persistência na nuvem | — | Disco efêmero, precisa exportar ou usar banco |

## Entrega

- Link do repositório GitHub.
- Link público do app no Streamlit Community Cloud.
- Print da interface Gradio rodando localmente.
- `gradio_app/pacientes.csv` de exemplo.
