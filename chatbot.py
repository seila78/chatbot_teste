import streamlit as st
from google import genai

# ================== CONFIGURAÇÃO DA PÁGINA ==================
st.set_page_config(
    page_title="Fulltech ChatBot",
    page_icon="🤖",
    layout="centered"
)

# ================== ESTILO (CSS) PERSONALIZADO ==================
st.markdown(f"""
<style>
    .stApp {{
        background-color: #f5f5f5;
    }}
    .stChatMessage {{
        border-radius: 15px;
        margin-bottom: 10px;
        color: #000000;
    }}
    [data-testid="stChatMessageUser"] {{
        background-color: #ffffff;
        border: 1px solid #14c204;
    }}
    [data-testid="stChatMessageAssistant"] {{
        background-color: #e0e0e0;
        border: 1px solid #000000;
    }}
    h2, p {{
        color: #000000 !important;
        text-align: center;
    }}
    hr {{
        border-top: 2px solid #14c204;
    }}
</style>
""", unsafe_allow_html=True)

# ================== SEGURANÇA E CLIENTE ==================
# Tenta pegar dos Secrets do Streamlit, senão usa a string direta
api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDX9MRX888fYTDYTY43KKJz24KSEJyAADo")

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
    # Adiciona mensagem do usuário ao estado
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        try:
            # Formata o histórico para o padrão do Google GenAI
            history = [
                {"role": m["role"], "parts": [{"text": m["content"]}]}
                for m in st.session_state.messages
            ]
            
            # Chamada correta para o modelo Gemini
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=history
            )
            
            full_response = response.text
            st.markdown(full_response)
            
            # Salva a resposta no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na API: {e}")