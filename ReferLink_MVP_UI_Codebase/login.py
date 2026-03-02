import streamlit as st
def login():
    role = st.selectbox("Login as",["Candidate","Referrer","Hiring Manager"])
    if st.button("Login"):
        st.session_state.role = role
        st.session_state.logged_in = True
