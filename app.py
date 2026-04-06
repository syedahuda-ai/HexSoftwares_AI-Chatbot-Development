import streamlit as st
import time
import os
from openai import OpenAI

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Virtual Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------- API SETUP --------------------
# Works with environment variable OR Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ API key not found! Please set OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background-color: #1f77ff;
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: right;
}

.bot-msg {
    background-color: #2a2d35;
    color: #e4e6eb;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: left;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #1f77ff;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="title">🤖 AI Virtual Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart NLP-based Chatbot with Real AI</div>', unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Settings")
    temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7)

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.info("Powered by OpenAI API")

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional AI customer support assistant. Be helpful, polite, and concise."}
    ]

# -------------------- AI RESPONSE FUNCTION --------------------
def get_ai_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! 👋 How can I help you today?"

    elif "price" in user_input:
        return "Our pricing depends on your needs. Please specify the product."

    elif "help" in user_input:
        return "Sure! Tell me your issue 😊"

    elif "bye" in user_input:
        return "Goodbye! Have a great day!"

    else:
        return "I'm a demo chatbot 🤖. Try asking about pricing or help!"
        ai_response = get_ai_response(user_input)

# -------------------- DISPLAY CHAT --------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INPUT --------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    st.markdown(f'<div class="user-msg">{user_input}</div>', unsafe_allow_html=True)

    # Generate AI response
    with st.spinner("🤖 Thinking..."):
        ai_response = get_ai_response()

    # Typing animation
    placeholder = st.empty()
    full_response = ""

    for char in ai_response:
        full_response += char
        placeholder.markdown(f'<div class="bot-msg">{full_response}</div>', unsafe_allow_html=True)
        time.sleep(0.01)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("🚀 AI Virtual Agent | Built with Streamlit + OpenAI")
