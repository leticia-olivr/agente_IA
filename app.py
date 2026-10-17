"""
Meu Primeiro Agente de IA com LLM
---------------------------------
Interface: Streamlit (chat no navegador)
Orquestração: LangChain
LLM: modelo aberto (GPT-OSS) hospedado na Groq, acessado via API
"""

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

# ---------------------------------------------------------------
# PASSO 1 - Carregar a chave da API que está no arquivo .env
# ---------------------------------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# ---------------------------------------------------------------
# PASSO 2 - Configurar a página (a "interface simples")
# ---------------------------------------------------------------
st.set_page_config(page_title="Meu Agente de IA", page_icon="🤖")
st.title("🤖 Meu Primeiro Agente de IA")
st.caption(f"LLM: {MODELO} (via Groq) • Orquestração: LangChain")

if not GROQ_API_KEY:
    st.error("Chave da API não encontrada. Crie o arquivo .env com GROQ_API_KEY=sua_chave")
    st.stop()

# ---------------------------------------------------------------
# PASSO 3 - Criar o "cérebro": o modelo de linguagem (LLM)
# temperature controla a criatividade (0 = mais preciso, 1 = mais criativo)
# ---------------------------------------------------------------
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODELO, temperature=0.7)

# ---------------------------------------------------------------
# PASSO 4 - Criar o prompt (as instruções do agente)
# - "system": define a personalidade/regras do agente
# - MessagesPlaceholder("historico"): onde entra a conversa anterior (CONTEXTO)
# - "human": a pergunta atual do usuário
# ---------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente prestativo e simpático. Responda sempre em português "
     "do Brasil, de forma clara e objetiva. Use o histórico da conversa para "
     "manter o contexto."),
    MessagesPlaceholder(variable_name="historico"),
    ("human", "{pergunta}"),
])

# ---------------------------------------------------------------
# PASSO 5 - Montar a "corrente" (chain) do LangChain:
# o prompt preenchido é enviado ao LLM
# ---------------------------------------------------------------
chain = prompt | llm

# ---------------------------------------------------------------
# PASSO 6 - Memória: guardamos o histórico na sessão do Streamlit
# (st.session_state persiste enquanto a página estiver aberta)
# ---------------------------------------------------------------
if "historico" not in st.session_state:
    st.session_state.historico = []

with st.sidebar:
    st.header("⚙️ Opções")
    if st.button("🗑️ Limpar conversa"):
        st.session_state.historico = []
        st.rerun()
    st.write(f"Mensagens na memória: {len(st.session_state.historico)}")

# Mostrar as mensagens antigas na tela
for msg in st.session_state.historico:
    papel = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(papel):
        st.markdown(msg.content)

# ---------------------------------------------------------------
# PASSO 7 - Receber a pergunta, chamar o agente e mostrar a resposta
# ---------------------------------------------------------------
pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        try:
            # stream() faz a resposta aparecer aos poucos, como no ChatGPT
            resposta = st.write_stream(
                pedaco.content
                for pedaco in chain.stream({
                    "historico": st.session_state.historico,
                    "pergunta": pergunta,
                })
            )
        except Exception as erro:
            st.error(f"Erro ao chamar o modelo: {erro}")
            st.stop()

    # Salvar pergunta e resposta na memória (é isso que mantém o contexto)
    st.session_state.historico.append(HumanMessage(content=pergunta))
    st.session_state.historico.append(AIMessage(content=resposta))
