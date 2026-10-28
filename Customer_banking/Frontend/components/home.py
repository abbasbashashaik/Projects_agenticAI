import streamlit as st
import httpx
def home():
    st.title("Banking Agent")
    api="http://127.0.0.1:8000/agent"
    # Initialize session state variable to store the report permanently across tabs
    if "screening_result" not in st.session_state:
        st.session_state.screening_result = None

    # Step A: Build Tabs
    Input, output, suggestions = st.tabs(["Inputs", "Outputs", "Suggestions"])
    query=st.chat_input("Ask any Question........")
    # Step B: Enter the Inputs Tab
    with Input:
        try:
            data={"query":query}
            response=httpx.post(f"{api}/chat",json=data,timeout=None)
            if response.status_code == 200:
                st.session_state.screening_result = response.json()
                st.success("Analysis complete! Check the 'Outputs' tab.")
            else:
                                    # Displays the raw error message if the URL or method is wrong
                st.error(f"Backend returned error code: {response.status_code}")
                st.text(response.text)
        except Exception as e:
                st.error(f"An error occurred during file parsing: {e}")
        
    with output:
        st.subheader("📋 Screening Results")
        if st.session_state.screening_result is not None:
            st.write(st.session_state.screening_result)
        else:
            st.info("No report generated yet. Submit the form in the 'Inputs' tab.")