import streamlit as st
import requests

def show():
    st.title("Referrer Dashboard")
    st.metric("Referral Score", 0)
    st.metric("Bonus Status", "Pending")

    st.subheader("Approve/Reject Referral Requests")
    try:
        referrals_response = requests.get("http://127.0.0.1:8000/referral_requests")
        if referrals_response.status_code == 200:
            referrals = referrals_response.json().get("referrals", [])
            for referral in referrals:
                st.write(f"Referral ID: {referral['id']}, Job ID: {referral['job_id']}, Referrer ID: {referral['referrer_id']}, Status: {referral['status']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve {referral['id']}"):
                        response = requests.post(
                            "http://127.0.0.1:8000/approve_referral",
                            json={"referral_id": referral['id']}
                        )
                        if response.status_code == 200:
                            st.success("Referral Approved")
                        else:
                            st.error(f"Failed to approve: {response.text}")
                with col2:
                    if st.button(f"Reject {referral['id']}"):
                        response = requests.post(
                            "http://127.0.0.1:8000/reject_referral",
                            json={"referral_id": referral['id']}
                        )
                        if response.status_code == 200:
                            st.success("Referral Rejected")
                        else:
                            st.error(f"Failed to reject: {response.text}")
        else:
            st.error("Failed to load referral requests.")
    except Exception as e:
        st.error(f"Error loading referrals: {e}")

    st.subheader("Earn Referral Score")
    referrer_id = st.text_input("Referrer ID for Score Update")
    if st.button("Update Referral Score"):
        if not referrer_id or not referrer_id.isdigit():
            st.error("Referrer ID must be an integer.")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/update_referral_score",
                    json={"referrer_id": int(referrer_id)}
                )
                if response.status_code == 200:
                    st.success("Referral Score Updated")
                else:
                    st.error(f"Failed to update score: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("View Bonus Status")
    try:
        bonus_response = requests.get("http://127.0.0.1:8000/bonus_status")
        if bonus_response.status_code == 200:
            bonus_status = bonus_response.json().get("status", "Unknown")
            st.info(f"Bonus Status: {bonus_status}")
        else:
            st.error("Failed to load bonus status.")
    except Exception as e:
        st.error(f"Error loading bonus status: {e}")