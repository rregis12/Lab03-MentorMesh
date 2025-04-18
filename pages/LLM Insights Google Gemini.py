import streamlit as st
import google.generativeai as genai
import requests
import random
import pandas as pd

st.set_page_config(page_title="LLM Mentor Insights", page_icon="🧠", layout="wide")
st.title("🧠 LLM Mentor Insights")
st.write("Compare and analyze top mentors using Google Gemini's advanced reasoning.")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")


    def fetch_mentors(num=10):
        response = requests.get(f"https://randomuser.me/api/?results={num}")
        if response.status_code == 200:
            data = response.json()['results']
            return [
                {
                    'name': f"{p['name']['first']} {p['name']['last']}",
                    'major': random.choice(["CS", "Psychology", "Engineering"]),
                    'experience': random.randint(1, 5),
                    'interests': random.sample(["Research", "Networking", "Leadership", "Internships"], 3),
                    'style': random.choice(["Informal", "Balanced", "Formal"]),
                    'rating': round(random.uniform(3.5, 5.0), 1)
                }
                for p in data
            ]
        return []

    if st.button("🔁 Refresh Mentor List"):
    st.session_state.mentors = fetch_mentors()
    
    if "mentors" not in st.session_state:
    st.session_state.mentors = fetch_mentors()

mentors = st.session_state.mentors


    mentor_names = [m['name'] for m in mentors]
    m1 = st.selectbox("Select Mentor 1", mentor_names)
    m2 = st.selectbox("Select Mentor 2", mentor_names)

    mentor1 = next((m for m in mentors if m["name"] == m1), None)
    mentor2 = next((m for m in mentors if m["name"] == m2), None)

    if mentor1 and mentor2 and st.button("🔍 Generate Insights"):
        prompt = f"""
Compare these two mentors for a peer mentorship match:

Mentor 1:
- Name: {mentor1['name']}
- Major: {mentor1['major']}
- Experience: {mentor1['experience']} years
- Interests: {', '.join(mentor1['interests'])}
- Communication Style: {mentor1['style']}
- Rating: {mentor1['rating']}

Mentor 2:
- Name: {mentor2['name']}
- Major: {mentor2['major']}
- Experience: {mentor2['experience']} years
- Interests: {', '.join(mentor2['interests'])}
- Communication Style: {mentor2['style']}
- Rating: {mentor2['rating']}

Which mentor might be a better match for a mentee interested in academic growth and career advice? Provide a detailed comparison and recommendation.
"""
        try:
            with st.spinner("Generating insights..."):
                response = model.generate_content(prompt)
                st.subheader("📝 Gemini's Recommendation")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error generating insights: {e}")
else:
    st.warning("Please enter your Gemini API key to continue.")
