import streamlit as st

st.set_page_config(page_title="MentorMesh", layout="wide")

st.title("MentorMesh: Peer Mentorship Platform")
st.subheader("CS 1301 Section A")
st.markdown("**Rashaun Regis**")

with st.container():
    st.write("Welcome to MentorMesh, a platform that connects students with peer mentors based on shared academic goals, interests, and communication styles.")
    st.markdown("""
    ### Navigation
    - **Home Page**: Learn what MentorMesh is all about.
    - **Mentor Matching**: Get matched with a compatible peer mentor.
    - **LLM Mentor Insights**: Use AI to compare and choose the best mentor.
    - **Mentor Chatbot**: Ask questions and get mentorship advice from our chatbot.
    """)

with st.container():
    st.header("🧠 Benefits of Peer Mentorship")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- Build a strong support system\n- Get real-world guidance\n- Learn from experienced peers")
    with col2:
        st.markdown("- Improve academic confidence\n- Develop professional skills\n- Get career direction")

st.image("Images/mentorship.jpg", use_column_width=True, caption="Empowering students through mentorship")

with st.container():
    st.header("🚀 How to Use MentorMesh")
    st.markdown("""
    1. Create your profile on the **Mentor Matching** page.
    2. View your top mentor matches.
    3. Use the **LLM Insights** page for AI-generated comparisons.
    4. Chat with the **Mentor Chatbot** for personalized advice.
    """)

