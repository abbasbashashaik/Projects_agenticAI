
import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000"


def get_api_client():
    if (
        "api_client" not in st.session_state
        or st.session_state.api_client is None
    ):
        st.session_state.api_client = httpx.Client(
            base_url=API_URL,
            timeout=30.0,
        )

    return st.session_state.api_client




def login():
    st.title("User Authentication Portal")

    with st.form("login_form"):
        username = st.text_input("Username or email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        client = get_api_client()

        try:
            response = client.post(
                "/auth/login",
                json={
                    "email_or_username": username,
                    "password": password,
                },
            )

            if response.status_code == 200:
                result = response.json()

                st.session_state.logged_in = True
                st.session_state.current_user = (
                    result["user"]["username"]
                )

                st.success("Login successful!")

                # Temporary diagnostic; do not print the cookie itself.
                st.write(
                    "Session cookie saved:",
                    "banking_session" in client.cookies,
                )

                st.rerun()

            else:
                st.error(
                    f"Login failed ({response.status_code}): "
                    f"{response.text}"
                )

        except httpx.RequestError as exc:
            st.error(f"Could not connect to FastAPI: {exc}")
