import streamlit as st
import httpx

api = "http://127.0.0.1:8000/auth"

def login():
    st.title("User Authentication Portal")
    with st.form(key="login_form",clear_on_submit=False):    
        username = st.text_input("enter username...")
        # Added type="password" to hide characters while typing
        password = st.text_input("enter password...", type="password") 
        submit_button=st.form_submit_button("Login")
    
    if submit_button:
        data = {"email_or_username": username, "password": password}
        
        try:
            response = httpx.post(f"{api}/login", json=data)
            
            # Check if the server responded with a successful status (200 OK)
            if response.status_code == 200:
                st.session_state.logged_in=True
                result = response.json()
                d=result["user"]
                st.write(result["message"],"logged username",d["username"])
                st.rerun()
            else:
                # Displays the raw error message if the URL or method is wrong
                st.error(f"Backend returned error code: {response.status_code}")
                st.text(response.text)
                
        except httpx.ConnectError:
            st.error("Cannot connect to FastAPI. Please verify that your backend server is running.")