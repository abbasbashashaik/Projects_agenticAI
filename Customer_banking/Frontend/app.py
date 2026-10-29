
import streamlit as st

from components.login import login
from components.register import register
from components.home import home


def logout():
    # Clear the server-side session through the backend
    client = st.session_state.get("api_client")

    if client is not None:
        try:
            client.post("/auth/logout")
        except Exception:
            pass
        finally:
            client.close()

    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.api_client = None
    st.session_state.chat_history = []
    st.session_state.screening_result = None

    st.rerun()


# Initialize Streamlit state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "api_client" not in st.session_state:
    st.session_state.api_client = None


if st.session_state.logged_in:
    st.sidebar.title("Navigation")
    st.sidebar.write(
        f"Logged in as: {st.session_state.current_user or 'User'}"
    )

    st.title("Banking Dashboard")
    st.write("You have successfully logged in.")

    query = st.chat_input("Ask your banking assistant...")

    # Run the chat page; None means no new message
    home(query or "")

    st.divider()

    if st.button("Log Out", type="primary"):
        logout()

else:
    page = st.sidebar.selectbox(
        "Navigation",
        ["Login", "Register"],
    )

    if page == "Login":
        st.subheader("Welcome Back!")
        login()

    elif page == "Register":
        st.subheader("Create a New Account")
        register()
