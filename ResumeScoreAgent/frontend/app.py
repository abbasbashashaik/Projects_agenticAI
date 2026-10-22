
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Welcome - My Streamlit App",
    page_icon="🔒",
    layout="centered"
)

# Initialize Session State for User Database & Authentication Status
if "users_db" not in st.session_state:
    # Pre-populating with a dummy user (Username: admin, Password: password123)
    st.session_state.users_db = {"admin": "password123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Helper function for logout
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()


# ==========================================
# MAIN APP VIEW (When user is logged in)
# ==========================================
if st.session_state.logged_in:
    st.title(f"👋 Welcome, {st.session_state.current_user}!")
    st.write("You have successfully logged in to the application.")
    
    st.success("This is your main dashboard / landing page content.")
    
    # Example Dashboard Content
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Active")
    col2.metric("Role", "Member")
    col3.metric("Session", "Live")
    
    st.divider()
    
    if st.button("Log Out", type="primary"):
        logout()

# ==========================================
# LOGIN / REGISTER VIEW (When user is logged out)
# ==========================================
else:
    st.title(" Welcome to Our Platform")
    st.subheader("Please log in or register to continue.")
    
    # Create Tabs for Login and Register
    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])
    
    # --- LOGIN TAB ---
    with tab_login:
        st.write("### Login to your account")
        
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if not login_username or not login_password:
                    st.warning("Please fill in both fields.")
                elif login_username in st.session_state.users_db and st.session_state.users_db[login_username] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = login_username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
    # --- REGISTER TAB ---
    with tab_register:
        st.write("### Create a new account")
        
        with st.form("register_form"):
            reg_username = st.text_input("Choose Username", key="reg_user")
            reg_password = st.text_input("Choose Password", type="password", key="reg_pass")
            reg_confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if not reg_username or not reg_password or not reg_confirm_pass:
                    st.warning("Please complete all required fields.")
                elif reg_username in st.session_state.users_db:
                    st.error("Username already exists! Please choose another one.")
                elif reg_password != reg_confirm_pass:
                    st.error("Passwords do not match.")
                elif len(reg_password) < 6:
                    st.warning("Password must be at least 6 characters long.")
                else:
                    # Save user to dictionary
                    st.session_state.users_db[reg_username] = reg_password
                    st.success("Account created successfully! You can now switch to the Login tab.")