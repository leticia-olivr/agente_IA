# 🤖 Meu Primeiro Agente de IA com LLM

Agente de IA que recebe perguntas em linguagem natural e responde usando um
Modelo de Linguagem de Grande Escala (LLM), mantendo o contexto da conversa.

## Tecnologias

| Componente | Ferramenta | Função |
|---|---|---|
| LLM | GPT-OSS 120B (modelo aberto, licença Apache 2.0) via API da [Groq](https://groq.com) | Gera as respostas |
| Orquestração | [LangChain](https://www.langchain.com/) | Monta o prompt, injeta o histórico e chama o LLM |
| Interface | [Streamlit](https://streamlit.io/) | Tela de chat no navegador |

## Como funciona

```
Usuário digita pergunta
        │
        ▼
 Prompt do LangChain = [instrução do sistema] + [histórico da conversa] + [pergunta]
        │
        ▼
 LLM (GPT-OSS na Groq) gera a resposta
        │
        ▼
 Resposta aparece na tela e é salva no histórico (memória/contexto)
```

A memória fica em `st.session_state.historico`: a cada nova pergunta, todas as
mensagens anteriores são enviadas junto ao modelo, por isso ele "lembra" da conversa.

## Como executar

1. Instale o Python 3.10+.
2. Crie uma chave gratuita em https://console.groq.com/keys
3. Copie `.env.example` para `.env` e cole a chave em `GROQ_API_KEY`.
4. No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run app.py
```

O navegador abre em http://localhost:8501.

## Teste de contexto (para a demonstração)

1. "Meu nome é Ana e eu estudo Engenharia."
2. "Qual é o meu nome e o que eu estudo?" → o agente deve lembrar.
