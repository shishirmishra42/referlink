from streamlit_option_menu import option_menu
import streamlit as st

def sidebar(role):
    with st.sidebar:
        selected = option_menu(
            "ReferLink Portal",
            ["Dashboard","Request Referral","Post Job"],
            icons=['house','person-check','briefcase'],
            menu_icon="cast",
            default_index=0,
        )
    return selected
