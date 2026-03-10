import streamlit as st
from google import genai

# ================== CONFIGURAÇÃO DA PÁGINA ==================
st.set_page_config(
    page_title="Fulltech ChatBot",
    page_icon="🤖",
    layout="centered"
)

# ================== ESTILO (CSS) PERSONALIZADO ==================
# Cores: Fundo (#f5f5f5), Texto/Detalhes (#000000), Destaque/Botões (#14c204)
st.markdown(f"""
<style>
    /* Fundo principal */
    .stApp {{
        background-color: #f5f5f5;
    }}

    /* Estilo das mensagens */
    .stChatMessage {{
        border-radius: 15px;
        margin-bottom: 10px;
        color: #000000;
    }}

    /* Mensagem do Usuário */
    [data-testid="stChatMessageUser"] {{
        background-color: #ffffff;
        border: 1px solid #14c204;
    }}

    /* Mensagem da IA */
    [data-testid="stChatMessageAssistant"] {{
        background-color: #e0e0e0;
        border: 1px solid #000000;
    }}

    /* Títulos e textos */
    h2, p {{
        color: #000000 !important;
        text-align: center;
    }}

    /* Cor do divisor */
    hr {{
        border-top: 2px solid #14c204;
    }}
</style>
""", unsafe_allow_html=True)

# ================== SEGURANÇA: OPENAI API KEY ==================
# Recomendado: Configure 'api_key' em Settings > Secrets no Streamlit Cloud
# O nome do secret deve ser: OPENAI_API_KEY
try:
    api_key = st.secrets["AIzaSyDX9MRX888fYTDYTY43KKJz24KSEJyAADo"]
except:
    api_key = "AIzaSyDX9MRX888fYTDYTY43KKJz24KSEJyAADo" # Fallback caso não use Secrets

client = genai.Client(api_key=api_key)

# ================== INTERFACE ==================
st.markdown("## 🤖 <span style='color:#14c204'>Fulltech</span> ChatBot", unsafe_allow_html=True)
st.markdown(
    "<p style='color: #000000;'>Converse com uma IA em tempo real</p>",
    unsafe_allow_html=True
)

st.divider()

# Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição do Histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de Entrada
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gemini-3-flash-preview",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erro na API: {e}")