import httpx
import streamlit as st

# Your FastAPI backend URL
api = "http://127.0.0.1:8000/auth"


def register():
  with st.form(key="register_form", clear_on_submit=False):
    username = st.text_input("Choose a username...")
    email = st.text_input("Enter your email...")
    password = st.text_input("Choose a password...", type="password")
    submit_button = st.form_submit_button("Register")

  if submit_button:
    data = {"username": username, "email": email, "password": password}

    try:
      response = httpx.post(f"{api}/register", json=data)

      # Check if the server responded with 201 Created
      if response.status_code == 201:
        st.success(
            "Registration successful! You can now log in using the sidebar."
        )
      else:
        st.error(f"Backend returned error code: {response.status_code}")
        st.text(response.text)

    except httpx.ConnectError:
      st.error(
          "Cannot connect to FastAPI. Please verify that your backend server is"
          " running."
      )