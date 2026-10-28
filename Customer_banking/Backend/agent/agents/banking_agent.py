from langchain_ollama import ChatOllama
from agent.tools_def.customer_tool import get_balance
from langgraph.prebuilt import create_react_agent

def ask_llm(query:str):
    tools = [get_balance]

    # 2. Initialize the Ollama model
    llm = ChatOllama(model="llama3.2", temperature=0)

    # 3. Bind the tools directly to the model
    # This creates a new model instance that is explicitly aware of your functions
    agent_executor = create_react_agent(llm,tools)

    # 4. Invoke the model directly
    # The model will output a ToolCall instead of a normal text response if it needs data

    if not query or query.strip() == "":
        return "Error: Empty query provided."

    # Send the query as a structured message history state
    inputs = {"messages": [("user", query)]}
    
    # LangGraph executes the tool dynamically behind the scenes
    agent_state = agent_executor.invoke(inputs)
    
    # Grab the very last message in the state (the final response from the LLM)
    final_message = agent_state["messages"][-1]
    
    # Return clean, un-nested text content back to your FastAPI router
    return final_message.content


    # print("AI Response Type:", type(response))
    # print("Tool Calls Selected by Llama:", response.tool_calls)