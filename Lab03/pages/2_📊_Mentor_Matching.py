import streamlit as st
import requests
import pandas as pd
import json
import random
from datetime import datetime
import plotly.express as px


st.set_page_config(page_title="Mentor Matching", page_icon="🤝", layout="wide")


st.title("🤝 Mentor Matching")
st.write("""
Find your ideal mentor match based on your interests, academic goals, and preferences.
Our matching algorithm analyzes profiles from our mentor database to connect you with 
experienced peers who can guide you on your academic journey.
""")


col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("Your Profile")
    
    
    st.subheader("Personal Information")
    name = st.text_input("Full Name", placeholder="Enter your name")
    
        st.subheader("Academic Information")
    
    
    
@st.cache_data
def get_majors():
    try:
        
        response = requests.get("https://api.academicpositions.com/majors")
        if response.status_code == 200:
            return sorted(response.json()['majors'])[:15]
        else:
            return ["Computer Science", "Biology", "Psychology", 
                   "Business", "Engineering"]  
    except Exception as e:
        st.error(f"Failed to fetch majors: {e}")
        return ["Computer Science", "Biology", "Psychology", 
               "Business", "Engineering"]

    majors = get_majors()
    selected_major = st.selectbox("Your Major", options=majors)
    
    year = st.selectbox("Academic Year", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])
    
   
    st.subheader("Interest Areas")
    interests = st.multiselect(
        "Select your interests (up to 5)",
        options=[
            "Academic Research", "Industry Internships", "Graduate School Preparation",
            "Career Networking", "Technical Skills", "Leadership Development",
            "Work-Life Balance", "Student Organizations", "Entrepreneurship",
            "Study Abroad", "Community Service", "Professional Certifications"
        ],
        max_selections=5
    )
    
    
    st.subheader("Mentorship Goals")
    goals = st.multiselect(
        "What do you hope to gain from mentorship? (up to 3)",
        options=[
            "Academic Guidance", "Career Advice", "Personal Development",
            "Networking Opportunities", "Research Experience", "Technical Skills",
            "Industry Insights", "Leadership Skills", "Work-Life Balance"
        ],
        max_selections=3
    )
    
   
    st.subheader("Preferences")
    communication_style = st.select_slider(
        "Communication Style",
        options=["Very Informal", "Somewhat Informal", "Balanced", "Somewhat Formal", "Very Formal"]
    )
    
    meeting_frequency = st.select_slider(
        "Preferred Meeting Frequency",
        options=["Weekly", "Bi-weekly", "Monthly", "As needed"]
    )
    
    
    submit_button = st.button("Find My Mentor Match")


@st.cache_data
def get_potential_mentors(num_mentors=20):
    try:
        response = requests.get(f"https://randomuser.me/api/?results={num_mentors}")
        if response.status_code == 200:
            mentors_data = response.json()['results']
            mentors = []
            
            
            all_majors = [
                "Computer Science", "Biology", "Psychology", "Business", 
                "Engineering", "Mathematics", "Physics", "Chemistry",
                "English", "History", "Economics", "Political Science"
            ]
            
            all_interests = [
                "Academic Research", "Industry Internships", "Graduate School Preparation",
                "Career Networking", "Technical Skills", "Leadership Development",
                "Work-Life Balance", "Student Organizations", "Entrepreneurship",
                "Study Abroad", "Community Service", "Professional Certifications"
            ]
            
            all_goals = [
                "Academic Guidance", "Career Advice", "Personal Development",
                "Networking Opportunities", "Research Experience", "Technical Skills",
                "Industry Insights", "Leadership Skills", "Work-Life Balance"
            ]
            
            communication_styles = ["Very Informal", "Somewhat Informal", "Balanced", "Somewhat Formal", "Very Formal"]
            meeting_frequencies = ["Weekly", "Bi-weekly", "Monthly", "As needed"]
            academic_years = ["Junior", "Senior", "Graduate", "PhD Candidate", "Alumni"]
            
            
            for mentor in mentors_data:
                mentor_majors = random.sample(all_majors, 1)[0]
                mentor_interests = random.sample(all_interests, random.randint(3, 5))
                mentor_goals = random.sample(all_goals, random.randint(2, 3))
                
                
                birth_date = datetime.strptime(mentor['dob']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                
                
                match_score = random.randint(25, 100)
                
                mentors.append({
                    'id': mentor['login']['uuid'],
                    'name': f"{mentor['name']['first']} {mentor['name']['last']}",
                    'picture': mentor['picture']['large'],
                    'email': mentor['email'],
                    'major': mentor_majors,
                    'academic_year': random.choice(academic_years),
                    'interests': mentor_interests,
                    'goals': mentor_goals,
                    'communication_style': random.choice(communication_styles),
                    'meeting_frequency': random.choice(meeting_frequencies),
                    'years_experience': random.randint(1, 5),
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'num_reviews': random.randint(1, 50),
                    'match_score': match_score
                })
            
            return mentors
        else:
            
            return generate_sample_mentors()
    except Exception as e:
        st.error(f"Failed to fetch mentor data: {e}")
        return generate_sample_mentors()


def generate_sample_mentors():
    sample_mentors = []
    for i in range(10):
        sample_mentors.append({
            'id': f"sample-{i}",
            'name': f"Sample Mentor {i+1}",
            'picture': "https://randomuser.me/api/portraits/men/1.jpg",
            'email': f"mentor{i+1}@example.com",
            'major': random.choice(["Computer Science", "Biology", "Psychology", "Business"]),
            'academic_year': random.choice(["Junior", "Senior", "Graduate", "PhD Candidate", "Alumni"]),
            'interests': random.sample([
                "Academic Research", "Industry Internships", "Graduate School Preparation",
                "Career Networking", "Technical Skills", "Leadership Development",
            ], 3),
            'goals': random.sample([
                "Academic Guidance", "Career Advice", "Personal Development",
                "Networking Opportunities", "Research Experience"
            ], 2),
            'communication_style': random.choice(["Very Informal", "Somewhat Informal", "Balanced", "Somewhat Formal", "Very Formal"]),
            'meeting_frequency': random.choice(["Weekly", "Bi-weekly", "Monthly", "As needed"]),
            'years_experience': random.randint(1, 5),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'num_reviews': random.randint(1, 50),
            'match_score': random.randint(25, 100)
        })
    return sample_mentors


def calculate_match_score(mentor, mentee_data):
    score = 0
    
    
    if mentor['major'] == mentee_data['major']:
        score += 25
    
    
    interest_matches = set(mentor['interests']).intersection(set(mentee_data['interests']))
    score += min(len(interest_matches) * 5, 25)
    
    
    goal_matches = set(mentor['goals']).intersection(set(mentee_data['goals']))
    score += min(len(goal_matches) * 8, 25)
    
    
    comm_styles = ["Very Informal", "Somewhat Informal", "Balanced", "Somewhat Formal", "Very Formal"]
    mentee_style_idx = comm_styles.index(mentee_data['communication_style'])
    mentor_style_idx = comm_styles.index(mentor['communication_style'])
    style_diff = abs(mentee_style_idx - mentor_style_idx)
    
    if style_diff == 0:
        score += 15
    elif style_diff == 1:
        score += 10  
    elif style_diff == 2:
        score += 5
    
    
    frequencies = ["Weekly", "Bi-weekly", "Monthly", "As needed"]
    mentee_freq_idx = frequencies.index(mentee_data['meeting_frequency'])
    mentor_freq_idx = frequencies.index(mentor['meeting_frequency'])
    freq_diff = abs(mentee_freq_idx - mentor_freq_idx)
    
    if freq_diff == 0:
        score += 10
    elif freq_diff == 1:
        score += 5
    
    return score


if 'submit_button' in locals() and submit_button and name:
    with col2:
        st.header("Potential Mentor Matches")
        
        
        all_mentors = get_potential_mentors(20)
        
       
        mentee_data = {
            'name': name,
            'major': selected_major,
            'academic_year': year,
            'interests': interests,
            'goals': goals,
            'communication_style': communication_style,
            'meeting_frequency': meeting_frequency
        }
        
        
        for mentor in all_mentors:
            match_score = calculate_match_score(mentor, mentee_data)
            mentor['match_score'] = match_score
            
        
        sorted_mentors = sorted(all_mentors, key=lambda x: x['match_score'], reverse=True)
        
        
        for i, mentor in enumerate(sorted_mentors[:5]):  
            st.subheader(f"Match #{i+1}: {mentor['name']}")
            
            
            m_col1, m_col2 = st.columns([1, 2])
            
            with m_col1:
                st.image(mentor['picture'], width=150)
                st.metric("Match Score", f"{mentor['match_score']}%")
                st.write(f"⭐ {mentor['rating']} ({mentor['num_reviews']} reviews)")
                
            with m_col2:
                st.write(f"**Major:** {mentor['major']}")
                st.write(f"**Academic Year:** {mentor['academic_year']}")
                st.write(f"**Years of Experience:** {mentor['years_experience']}")
                st.write(f"**Communication Style:** {mentor['communication_style']}")
                st.write(f"**Meeting Frequency:** {mentor['meeting_frequency']}")
                
                st.write("**Interests:**")
                for interest in mentor['interests']:
                    st.write(f"- {interest}")
                    
                
                matching_interests = set(mentor['interests']).intersection(set(interests))
                if matching_interests:
                    st.write("**Matching Interests:**")
                    for match in matching_interests:
                        st.write(f"- {match} 🔍")
            
            
            if st.button(f"Connect with {mentor['name']}", key=f"connect_{i}"):
                st.success(f"Request sent to {mentor['name']}! You'll receive a notification when they respond.")
            
            st.divider()
        
        
        st.header("Compatibility Analysis")
        
        
        mentors_df = pd.DataFrame([
            {
                'Mentor': mentor['name'], 
                'Match Score': mentor['match_score'],
                'Major': mentor['major'],
                'Years Experience': mentor['years_experience'],
                'Rating': mentor['rating']
            } for mentor in sorted_mentors[:8]  
        ])
        
        
        fig = px.bar(
            mentors_df, 
            x='Mentor', 
            y='Match Score',
            color='Match Score',
            color_continuous_scale='Viridis',
            labels={'Match Score': 'Compatibility (%)'},
            title='Mentor Compatibility Comparison'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        
        fig2 = px.scatter(
            mentors_df, 
            x="Years Experience", 
            y="Rating", 
            size="Match Score", 
            color="Match Score",
            hover_name="Mentor",
            size_max=30,
            color_continuous_scale='Viridis',
            title='Mentor Experience vs. Rating'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        
        def convert_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            "Download Mentor Matches CSV",
            convert_to_csv(mentors_df),
            "mentor_matches.csv",
            "text/csv",
            key='download-csv'
        )
elif 'submit_button' in locals() and submit_button and not name:
    with col2:
        st.error("Please enter your name to find mentor matches.")


st.sidebar.title("Mentorship Tips")
st.sidebar.write("""
### Making the Most of Mentorship
1. **Be Proactive**: Reach out regularly and come prepared with questions
2. **Set Clear Goals**: Define what you want to achieve from the relationship
3. **Be Respectful**: Value your mentor's time and insights
4. **Provide Updates**: Share your progress and how their advice helped
5. **Express Gratitude**: Thank your mentor for their guidance
""")


st.sidebar.title("Student Testimonials")
testimonials = [
    {"name": "Jamie L.", "text": "The mentor matching algorithm connected me with someone who truly understood my goals. Six months later, I've secured my dream internship thanks to their guidance."},
    {"name": "Alex P.", "text": "Having a mentor who had already navigated the same challenges I was facing made all the difference in my academic journey."},
    {"name": "Sam T.", "text": "My mentor helped me develop not just academically, but professionally too. The skills I've gained are invaluable."}
]

testimonial = random.choice(testimonials)
st.sidebar.markdown(f"*\"{testimonial['text']}\"*")
st.sidebar.markdown(f"**— {testimonial['name']}**")
