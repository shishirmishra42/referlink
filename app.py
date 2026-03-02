import streamlit as st
from ui.sidebar import sidebar
import login
from ui import candidate_dashboard, manager_dashboard, referrer_dashboard, admin_dashboard

st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.login()
else:
    role = st.session_state.role
    selected = sidebar(role)
    if role == "Candidate":
        candidate_dashboard.show()
    elif role == "Hiring Manager":
        manager_dashboard.show()
    elif role == "Referrer":
        referrer_dashboard.show()
    elif role == "Admin":
        admin_dashboard.show()
