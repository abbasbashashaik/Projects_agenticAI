
import streamlit as st
import httpx
from components.login import get_api_client

def home(query: str):
    st.title("Banking Agent")

    # FastAPI endpoint
    api_path = "/agent/chat"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "screening_result" not in st.session_state:
        st.session_state.screening_result = None

    Input, output, suggestions = st.tabs(
        ["Inputs & Chat", "Outputs", "Suggestions"]
    )

    with Input:
        # Display existing messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if query and query.strip():
            query = query.strip()

            # Avoid processing the same query twice
            is_new_query = (
                not st.session_state.chat_history
                or st.session_state.chat_history[-1]["content"] != query
                or st.session_state.chat_history[-1]["role"] != "user"
            )

            if is_new_query:
                with st.chat_message("user"):
                    st.write(query)

                st.session_state.chat_history.append(
                    {"role": "user", "content": query}
                )

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing banking data..."):
                        try:
                            # Reuse the client from the login function
                            client = st.session_state.get("api_client")

                            if client is None:
                                raise RuntimeError(
                                    "API session is missing. Please log in again."
                                )
                            client=get_api_client()
    
                            response = client.post(
                                api_path,
                                json={"query": query},
                                timeout=None,
                            )

                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.screening_result = result

                                bot_reply = str(result)
                                st.write(bot_reply)

                                st.session_state.chat_history.append(
                                    {
                                        "role": "assistant",
                                        "content": bot_reply,
                                    }
                                )

                                st.success(
                                    "Analysis complete! Check the Outputs tab."
                                )

                            elif response.status_code == 401:
                                st.session_state.logged_in = False

                                error_msg = (
                                    "Your login session is missing or expired. "
                                    "Please log in again."
                                )
                                st.error(error_msg)

                                st.session_state.chat_history.append(
                                    {
                                        "role": "assistant",
                                        "content": f"⚠️ {error_msg}",
                                    }
                                )

                            else:
                                error_msg = (
                                    f"Backend returned error code: "
                                    f"{response.status_code}\n"
                                    f"{response.text}"
                                )
                                st.error(error_msg)

                                st.session_state.chat_history.append(
                                    {
                                        "role": "assistant",
                                        "content": f"⚠️ {error_msg}",
                                    }
                                )

                        except (httpx.RequestError, RuntimeError) as e:
                            error_msg = f"Request failed: {e}"
                            st.error(error_msg)

                            st.session_state.chat_history.append(
                                {
                                    "role": "assistant",
                                    "content": f"⚠️ {error_msg}",
                                }
                            )

                st.rerun()

    with output:
        st.subheader("📋 Screening Results")

        if st.session_state.screening_result is not None:
            st.write(st.session_state.screening_result)
        else:
            st.info(
                "No report generated yet. Ask a question in the chat."
            )

    with suggestions:
        st.subheader("Suggestions")
        st.write("Try asking: Get my customer details.")
