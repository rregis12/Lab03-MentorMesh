import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mentor Chatbot", page_icon="💬", layout="wide")
st.title("💬 Mentor Chatbot Assistant")
st.write("Ask our AI Mentor anything about planning, goals, or finding the right match!")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    # ✅ UPDATED MODEL NAME
    model = genai.GenerativeModel("gemini-2.5-pro")

    # Chat session setup
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    user_input = st.text_input("Ask your mentorship question:")

    if user_input:
        try:
            response = st.session_state.chat.send_message(user_input)
            st.chat_message("user").markdown(user_input)
            st.chat_message("assistant").markdown(response.text)
        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")
else:
    st.warning("Please enter your Gemini API key to continue.")



