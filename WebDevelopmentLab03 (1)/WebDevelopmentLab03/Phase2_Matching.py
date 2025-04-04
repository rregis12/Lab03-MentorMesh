import streamlit as st
import requests
import pandas as pd

st.title("Mentor Matching")
st.write("Find your ideal mentor based on shared interests and academic goals.")

def fetch_profiles(num_users=10):
    try:
        response = requests.get(f"https://randomuser.me/api/?results={num_users}")
        response.raise_for_status()  
        data = response.json()
        profiles = []
        for user in data["results"]:
            profiles.append({
                "name": f"{user['name']['first']} {user['name']['last']}",
                "location": f"{user['location']['city']}, {user['location']['country']}",  
                "interests": "CS, Robotics, AI",
                "goals": "Internships, Research"
            })
        return pd.DataFrame(profiles)
    except Exception as e:
        st.error(f"Failed to fetch profiles: {str(e)}")
        return pd.DataFrame()  

def match_users(mentee_interests, mentee_goals, mentors_df):
    mentors_df["score"] = mentors_df.apply(
        
        lambda row: len(set(mentee_interests) & set(row["interests"].split(", "))) +
                    len(set(mentee_goals) & set(row["goals"].split(", "))),
        axis=1
    )
    return mentors_df.sort_values("score", ascending=False)


interests = st.multiselect("Your interests", ["CS", "Robotics", "AI", "Data Science"])
goals = st.multiselect("Your goals", ["Internships", "Research", "Graduate School"])

if st.button("Find Matches"):
    mentors_df = fetch_profiles()
    
    if not mentors_df.empty:  
        matches = match_users(interests, goals, mentors_df)
        
        st.subheader("Top Matches")
        st.dataframe(matches[["name", "location", "interests", "goals", "score"]], 
                    hide_index=True)
        
        st.bar_chart(matches.set_index("name")["score"])
