import streamlit as st
import requests

def show():
    st.title("Admin Dashboard")
    st.subheader("User Management")
    user_email = st.text_input("User Email")
    action = st.selectbox("Action", ["Activate", "Deactivate", "Delete"])
    if st.button("Manage User"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/manage_user",
                json={"email": user_email, "action": action}
            )
            if response.status_code == 200:
                st.success("User management action successful.")
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Job Moderation")
    job_id = st.text_input("Job ID for Moderation")
    moderation_action = st.selectbox("Moderation Action", ["Approve", "Reject", "Delete"])
    if st.button("Moderate Job"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/moderate_job",
                json={"job_id": job_id, "action": moderation_action}
            )
            if response.status_code == 200:
                st.success("Job moderation successful.")
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Fraud Detection")
    if st.button("Run Fraud Detection"):
        try:
            response = requests.post("http://127.0.0.1:8000/fraud_detection")
            if response.status_code == 200:
                st.success("Fraud detection completed.")
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Referral Audit")
    referral_id = st.text_input("Referral ID for Audit")
    if st.button("Audit Referral"):
        try:
            response = requests.get(f"http://127.0.0.1:8000/referral_audit/{referral_id}")
            if response.status_code == 200:
                audit = response.json().get("audit", {})
                st.write(audit)
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Score Reset")
    reset_user_id = st.text_input("User ID for Score Reset")
    if st.button("Reset Score"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/reset_score",
                json={"user_id": reset_user_id}
            )
            if response.status_code == 200:
                st.success("Score reset successful.")
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
# ...existing code...
