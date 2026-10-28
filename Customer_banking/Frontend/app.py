import streamlit as st
from components.login import login
from components.register import register

from components.login import login
from components.register import register
from components.home import home
import streamlit as st

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()



# Sidebar navigation to switch between Login and Register
page = st.sidebar.selectbox("Navigation", ["Login", "Register"])
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Helper function for logout

if st.session_state.logged_in:
    # st.title(f"👋 Welcome, {st.session_state.current_user}!")
    st.write("You have successfully logged in to the application.")
    
    st.success("This is your main dashboard / landing page content.")
    home()
    # # Example Dashboard Content
    # col1, col2, col3 = st.columns(3)
    # col1.metric("Status", "Active")
    # col2.metric("Role", "Member")
    # col3.metric("Session", "Live")
    
    st.divider()
    
    if st.button("Log Out", type="primary"):
        logout()
else:
    if page == "Login":
        st.subheader("Welcome Back!")
        login()
    
    elif page == "Register":
        st.subheader("Create a New Account")
        register()
        