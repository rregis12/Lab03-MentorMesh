import streamlit as st

# Title of App
st.title("MentorMesh")

# Assignment Data 
# TODO: Rashaun Regis, Section A Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team XX, Web Development - Section A")
st.subheader("Rashaun Regis")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Home Page**: Introduction to our mentorship platform connecting students with experienced mentors.
#       2. **Mentor Matching Page**: Uses academic interests and goals data to find optimal mentor matches.
#       3. **Mentorship Analytics Page**: Visualizes mentorship data to track progress and engagement.
#       4. **AI Mentor Assistant**: Get personalized mentorship advice using Google Gemini.


st.write("""
Welcome to our Peer Mentorship Platform! This application helps connect new students with experienced mentors based on shared interests, academic goals, and career aspirations. Navigate between the pages using the sidebar to the left. The following pages are available:

1. Home Page: Introduction to our mentorship platform connecting students with experienced mentors.
2. Mentor Matching Page : Uses academic interests and goals data to find optimal mentor matches.
3. Mentorship Analytics Page: Visualizes mentorship data to track progress and engagement.
4. AI Mentor Assistant: Get personalized mentorship advice using Google Gemini.

         
""")

st.divider()
st.subheader("Navigate to Pages")
st.page_link("Home_Page.py", label="Home")
st.page_link("Phase2_Matching.py", label="Mentor Matching")
st.page_link("Phase3_LLM_Analysis.py", label="Analytics")
st.page_link("Phase4_Chatbot.py", label="AI Assistant")

st.image("Images/mentorship.jpg", caption="Building connections through mentorship", use_column_width=True)


st.header("Benefits of Peer Mentorship")
st.write("""
Peer mentorship programs offer numerous benefits for both mentors and mentees:

- **Knowledge Transfer**: Share experiences and insights that aren't found in textbooks
- **Network Building**: Expand your professional and academic connections
- **Skill Development**: Develop leadership and communication skills
- **Support System**: Create a supportive environment for academic and personal growth
- **Career Guidance**: Get practical advice on career paths and opportunities
""")


st.header("How Our Platform Works")
st.write("""
1. **Create a Profile**: Fill out your interests, academic goals, and mentorship preferences
2. **Get Matched**: Our algorithm connects you with compatible mentors or mentees
3. **Set Goals**: Establish clear objectives for your mentorship relationship
4. **Track Progress**: Monitor achievements and growth throughout the mentorship
5. **Communicate**: Stay connected through our built-in communication tools
""")

