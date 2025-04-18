import streamlit as st
import requests
import pandas as pd
import random
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Mentor Matching", page_icon="🤝", layout="wide")

st.title("🤝 Mentor Matching")
st.write("Get matched with a mentor who shares your goals and supports your academic journey.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("Your Profile")
    name = st.text_input("Full Name")
    year = st.selectbox("Academic Year", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])

    @st.cache_data
    def get_majors():
        try:
            response = requests.get("https://api.sampleapis.com/futurama/characters")
            if response.status_code == 200:
                occupations = [char['occupation'] for char in response.json() if char.get('occupation')]
                return list(set(occupations))[:15] + ["Computer Science", "Biology", "Psychology"]
        except:
            return ["Computer Science", "Biology", "Psychology", "Engineering"]
        return ["Computer Science", "Biology"]

    majors = get_majors()
    selected_major = st.selectbox("Your Major", majors)

    interests = st.multiselect("Select your interests (up to 5)", [
        "Academic Research", "Industry Internships", "Graduate School Preparation",
        "Career Networking", "Technical Skills", "Leadership Development",
        "Work-Life Balance", "Student Organizations", "Entrepreneurship",
        "Study Abroad", "Community Service", "Professional Certifications"
    ], max_selections=5)

    goals = st.multiselect("Mentorship Goals (up to 3)", [
        "Academic Guidance", "Career Advice", "Personal Development",
        "Networking Opportunities", "Research Experience", "Technical Skills",
        "Industry Insights", "Leadership Skills", "Work-Life Balance"
    ], max_selections=3)

    communication_style = st.select_slider("Communication Style", [
        "Very Informal", "Somewhat Informal", "Balanced", "Somewhat Formal", "Very Formal"
    ])
    meeting_frequency = st.select_slider("Meeting Frequency", [
        "Weekly", "Bi-weekly", "Monthly", "As needed"
    ])
    submit_button = st.button("Find My Mentor Match")

@st.cache_data
def get_mentors(n=20):
    try:
        r = requests.get(f"https://randomuser.me/api/?results={n}")
        if r.status_code == 200:
            raw = r.json()['results']
            return [{
                'id': p['login']['uuid'],
                'name': f"{p['name']['first']} {p['name']['last']}",
                'picture': p['picture']['large'],
                'email': p['email'],
                'major': random.choice(["Computer Science", "Biology", "Engineering"]),
                'academic_year': random.choice(["Junior", "Senior", "Graduate"]),
                'interests': random.sample(interests, 3),
                'goals': random.sample(goals, 2),
                'communication_style': random.choice(["Very Informal", "Balanced", "Very Formal"]),
                'meeting_frequency': random.choice(["Weekly", "Monthly"]),
                'years_experience': random.randint(1, 5),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'match_score': random.randint(50, 100)
            } for p in raw]
    except:
        return []
    return []

def calculate_score(mentor, user):
    score = 0
    if mentor['major'] == user['major']:
        score += 20
    score += len(set(mentor['interests']) & set(user['interests'])) * 5
    score += len(set(mentor['goals']) & set(user['goals'])) * 6
    if mentor['communication_style'] == user['communication_style']:
        score += 10
    if mentor['meeting_frequency'] == user['meeting_frequency']:
        score += 10
    return score

if submit_button and name:
    with col2:
        st.header("Your Top Matches")
        user_profile = {
            'name': name,
            'major': selected_major,
            'academic_year': year,
            'interests': interests,
            'goals': goals,
            'communication_style': communication_style,
            'meeting_frequency': meeting_frequency
        }
        mentors = get_mentors()
        for m in mentors:
            m['match_score'] = calculate_score(m, user_profile)
        top_matches = sorted(mentors, key=lambda x: x['match_score'], reverse=True)[:5]

        for i, m in enumerate(top_matches):
            st.subheader(f"Match #{i+1}: {m['name']}")
            pic, info = st.columns([1, 2])
            with pic:
                st.image(m['picture'], width=120)
                st.metric("Match", f"{m['match_score']}%")
                st.write(f"{m['rating']} ⭐")
            with info:
                st.write(f"Major: {m['major']} | Year: {m['academic_year']}")
                st.write(f"Experience: {m['years_experience']} years")
                st.write("Interests: " + ", ".join(m['interests']))
                st.write("Goals: " + ", ".join(m['goals']))
            st.divider()

        df = pd.DataFrame([{
            "Mentor": m['name'],
            "Match Score": m['match_score'],
            "Experience": m['years_experience'],
            "Rating": m['rating']
        } for m in top_matches])
        fig = px.bar(df, x="Mentor", y="Match Score", color="Match Score", title="Top Mentor Scores")
        st.plotly_chart(fig, use_container_width=True)
else:
    if submit_button:
        with col2:
            st.error("Please enter your name.")

