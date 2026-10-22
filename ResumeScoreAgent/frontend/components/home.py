import streamlit as st
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
import tempfile
import pypdf
import httpx
def home():
    st.title("Resume Screening Agent")
    api="http://127.0.0.1:8000/agent"
    # Initialize session state variable to store the report permanently across tabs
    if "screening_result" not in st.session_state:
        st.session_state.screening_result = None

    # Step A: Build Tabs
    Input, output, suggestions = st.tabs(["Inputs", "Outputs", "Suggestions"])
    
    # Step B: Enter the Inputs Tab
    with Input:
        st.subheader("Provide Job Details & Resume")
        
        # Step C: Put the Form Container inside the Tab
        with st.form(key="screening_form"):
            
            # Step D: Split into two columns inside the form
            description_col, resume_col = st.columns(2)
            
            with description_col:
                query = st.text_area("Paste your job description here...", height=250)
                
            with resume_col:
                document = st.file_uploader(label="Upload Resume", type=["docx", "pdf", "txt"])
            
            # Step E: Single Submit Button at the bottom of the columns
            submit_button = st.form_submit_button(label="🚀 Run Screening Agent", use_container_width=True)
        
        # Step F: Form Submission Handling Logic
        if submit_button:
            if not query:
                st.error("Please paste a job description first!")
            elif not document:
                st.error("Please upload a resume file first!")
            else:
                with st.spinner("Extracting documents and running screening crew..."):
                    file_extension = document.name.split(".")[-1].lower()
                    
                    try:
                        # Save uploaded file stream into a readable temp file for LangChain
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                            temp_file.write(document.read())
                            temp_file_path = temp_file.name
                        
                        # Use appropriate LangChain loader based on file extension
                        if file_extension == "pdf":
                            from langchain_community.document_loaders import PyPDFLoader
                            loader = PyPDFLoader(temp_file_path)
                            resume_txt = "\n".join([p.page_content for p in loader.load()])
                        elif file_extension == "docx":
                            from langchain_community.document_loaders import Docx2txtLoader
                            loader = Docx2txtLoader(temp_file_path)
                            resume_txt = loader.load()[0].page_content
                        elif file_extension == "txt":
                            from langchain_community.document_loaders import TextLoader
                            loader = TextLoader(temp_file_path, encoding="utf-8")
                            resume_txt = loader.load()[0].page_content
                        data={"job_description":query,"resume_txt":resume_txt}
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
            st.write(st.session_state.screening_result["result"])
        else:
            st.info("No report generated yet. Submit the form in the 'Inputs' tab.")

