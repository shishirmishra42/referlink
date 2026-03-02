import streamlit as st
import requests

def show():
    st.title("Candidate Dashboard")
    st.metric("Referrals Requested",5)
    st.metric("Approved",2)
    st.metric("Interview Calls",1)

    st.subheader("Create Profile")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Save Profile"):
        if not name or not email:
            st.error("Name and Email are required.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/create_profile",
                    json={"name": name, "email": email}
                )
                if response.status_code == 200:
                    st.success("Profile saved.")
                else:
                    st.error(f"Failed to save profile: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Add Work History")
    company = st.text_input("Company Name")
    position = st.text_input("Position")
    years = st.number_input("Years Worked", min_value=0, step=1)
    if st.button("Add Work History"):
        if not company or not position:
            st.error("Company and Position are required.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/add_work_history",
                    json={"company": company, "position": position, "years": years}
                )
                if response.status_code == 200:
                    st.success("Work history added.")
                else:
                    st.error(f"Failed to add work history: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Add Skills")
    skill = st.text_input("Skill")
    if st.button("Add Skill"):
        if not skill:
            st.error("Skill is required.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/add_skill",
                    json={"skill": skill}
                )
                if response.status_code == 200:
                    st.success("Skill added.")
                else:
                    st.error(f"Failed to add skill: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Add Connections")
    connection_email = st.text_input("Connection Email")
    if st.button("Add Connection"):
        if not connection_email:
            st.error("Connection Email is required.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/add_connection",
                    json={"connection_email": connection_email}
                )
                if response.status_code == 200:
                    st.success("Connection added.")
                else:
                    st.error(f"Failed to add connection: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("View Jobs")
    try:
        jobs_response = requests.get("http://127.0.0.1:8000/jobs")
        if jobs_response.status_code == 200:
            jobs = jobs_response.json().get("jobs", [])
            for job in jobs:
                st.write(f"Job ID: {job['id']}, Title: {job['job_title']}, Company: {job['company']}, Skills: {job['skills']}, Bonus: {job['bonus']}")
        else:
            st.error("Failed to load jobs.")
    except Exception as e:
        st.error(f"Error loading jobs: {e}")

    st.subheader("Request Referral")
    job_id = st.text_input("Enter Job ID")
    referrer_id = st.text_input("Enter Referrer ID")
    if st.button("Request"):
        if not job_id or not referrer_id:
            st.error("Both Job ID and Referrer ID are required.")
        elif not referrer_id.isdigit():
            st.error("Referrer ID must be an integer.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/request_referral",
                    json={"job_id": job_id, "referrer_id": int(referrer_id)}
                )
                if response.status_code == 200:
                    st.success("Referral Requested")
                else:
                    st.error(f"Failed to request referral: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Track Application")
    application_id = st.text_input("Application ID")
    if st.button("Track Application"):
        if not application_id:
            st.error("Application ID is required.")
        else:
            try:
                response = requests.get(f"http://127.0.0.1:8000/track_application/{application_id}")
                if response.status_code == 200:
                    status = response.json().get("status", "Unknown")
                    st.info(f"Application Status: {status}")
                else:
                    st.error(f"Failed to track application: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Submit Application")
    app_status = st.text_input("Application Status", value="Submitted")
    if st.button("Submit Application"):
        if not app_status:
            st.error("Application status is required.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/submit_application",
                    json={"status": app_status}
                )
                if response.status_code == 200:
                    app_id = response.json().get("application_id")
                    st.success(f"Application submitted! Your Application ID is {app_id}.")
                else:
                    st.error(f"Failed to submit application: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
