# streamlit - frontend e backend
import streamlit as st
from openai import OpenAI

# ================== CONFIGURAÇÃO DA PÁGINA ==================
st.set_page_config(
    page_title="ChatBot com IA",
    page_icon="🤖",
    layout="centered"
)

# ================== ESTILO (CSS) ==================
st.markdown("""
<style>
    body {
        background-color: #0f172a;
    }

    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #1e293b;
    }

    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #020617;
        border: 1px solid #1e293b;
    }

    h1, h2, h3 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ================== OPENAI ==================
modelo = OpenAI(api_key="COLOQUE_SUA_API_KEY_AQUI")

# ================== TÍTULO ==================
st.markdown("## 🤖 ChatBot com IA")
st.markdown(
    "<p style='text-align:center; color: #94a3b8;'>Converse com uma IA em tempo real</p>",
    unsafe_allow_html=True
)

st.divider()

# session state
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []

# historico de mensagens
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)

# caixa de input
mensagem_usuario = st.chat_input("Digite sua mensagem...")

if mensagem_usuario:
    # mensagem do usuário
    st.chat_message("user").write(mensagem_usuario)
    mensagem = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem)

    # resposta da IA
    resposta_modelo = modelo.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gpt-4o"
    )

    resposta_ia = resposta_modelo.choices[0].message.content

    # mensagem da IA
    st.chat_message("assistant").write(resposta_ia)
    mensagem_ia = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)
