import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BaristaAI - Ekosistem Bisnis Kopi", page_icon="☕")
st.title("☕ BaristaAI: Asisten Smart Bisnis Kopi")
st.caption("Chatbot Ekosistem Bisnis Kopi Terintegrasi Google Gemini API")

api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

if not api_key:
    st.info("Silakan masukkan Google Gemini API Key Anda untuk memulai.")
    st.stop()

genai.configure(api_key=api_key)

model_choice = st.sidebar.selectbox("Pilih Model Gemini:", ["gemini-2.5-flash", "gemini-2.5-pro"])
temperature = st.sidebar.slider("Temperature:", 0.0, 2.0, 0.7)

persona = st.sidebar.radio("Pilih Persona:", ["Pelanggan (Virtual Barista)", "Pemilik Kedai (Konsultan Bisnis)"])

if "Pelanggan" in persona:
    system_instruction = "Anda adalah BaristaAI, seorang barista ramah yang paham tentang kopi dan resep minuman."
else:
    system_instruction = "Anda adalah Konsultan Bisnis Kopi profesional yang membantu operasional dan marketing kedai kopi."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Tanyakan sesuatu tentang kopi...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    full_prompt = f"{system_instruction}\n\nPertanyaan: {user_input}"
    generation_config = genai.types.GenerationConfig(temperature=temperature)
    model = genai.GenerativeModel(model_name=model_choice, generation_config=generation_config)

    with st.chat_message("assistant"):
        with st.spinner("Berpikir..."):
            try:
                response = model.generate_content(full_prompt)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {str(e)}")
