import streamlit as st
import requests

def show():
    st.title("Hiring Manager Dashboard")
    st.subheader("Post Job")
    company = st.text_input("Company")
    role = st.text_input("Job Role")
    skills = st.text_input("Skills")
    bonus = st.number_input("Referral Bonus")
    if st.button("Post Job"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/create_job",
                json={"company": company, "job_title": role, "skills": skills, "bonus": int(bonus)}
            )
            if response.status_code == 200:
                st.success("Job posted successfully!")
            else:
                st.error(f"Failed to post job: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Set Referral Bonus")
    job_id = st.text_input("Job ID for Bonus")
    new_bonus = st.number_input("New Referral Bonus")
    if st.button("Update Bonus"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/update_bonus",
                json={"job_id": job_id, "bonus": int(new_bonus)}
            )
            if response.status_code == 200:
                st.success("Bonus updated.")
            else:
                st.error(f"Failed to update bonus: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Filter Candidates")
    score = st.number_input("Minimum Referrer Score")
    if st.button("Filter by Score"):
        try:
            response = requests.get(f"http://127.0.0.1:8000/filter_candidates?score={score}")
            if response.status_code == 200:
                candidates = response.json().get("candidates", [])
                for candidate in candidates:
                    st.write(f"Candidate: {candidate['name']}, Score: {candidate['score']}")
            else:
                st.error(f"Failed to filter candidates: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Mutual Organization/Project History")
    candidate_id = st.text_input("Candidate ID for Mutual Org/Project")
    if st.button("View Mutual History"):
        try:
            response = requests.get(f"http://127.0.0.1:8000/mutual_history/{candidate_id}")
            if response.status_code == 200:
                history = response.json().get("history", [])
                for item in history:
                    st.write(item)
            else:
                st.error(f"Failed to load history: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
