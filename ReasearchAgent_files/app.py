# import os
# from langchain_community.utilities.powerbi import PowerBIDataset
# from langchain_community.agent_toolkits.powerbi.toolkit import PowerBIToolkit
# from langchain_community.agent_toolkits.powerbi.base import create_pbi_agent

# # 1. FIX THE VALIDATION: Import the Azure token generation utilities
# from azure.identity import DefaultAzureCredential
# from azure.core.credentials import TokenCredential

# # Resolve Pydantic validation mapping
# PowerBIDataset.model_rebuild()

# # 2. GENERATE THE AUTHENTICATION TOKEN
# # This will automatically pick up your 'az login' credentials from your terminal
# azure_credential = DefaultAzureCredential()

# workspace_id = "9ce610b6-7b08-4763-90e0-cc1903dedfa6"
# dataset_id = "0d93f6fb-67aa-403f-90e9-4df9f0c4e8b3"

# # 3. INITIALIZE THE DATASET WITH THE CREDENTIAL OBJECT
# pbi_dataset = PowerBIDataset(
#     dataset_id=dataset_id,
#     workspace_id=workspace_id,
#     credential=azure_credential,  # <-- This satisfies the validation requirement
#     table_names=["gold_dim_supplier","gold_inventory_dashboard","gold_supplier_performance"]
# )

# # 4. FIX THE LLM: Use LangChain's ChatOllama wrapper instead of pure ollama library
# # Make sure you run: pip install langchain-ollama
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.2", temperature=0)

# # 5. Bind the components together into the agent toolkit
# pbi_toolkit = PowerBIToolkit(
#     powerbi=pbi_dataset, 
#     llm=llm
# )

# # 6. Build the analytical agent
# agent_executor = create_pbi_agent(
#     llm=llm,
#     toolkit=pbi_toolkit,
#     verbose=True,
#     max_iterations=20,
#     early_stopping_method="generate"
# )
# print("Connected tables:", pbi_dataset.get_table_names())
# # # 7. Execute your query
# query = "list the available tables and give me the count of rows of each table."
# response = agent_executor.invoke({"input": query})
# # Temporary debug test to see if Azure actually sees tables


# print("\n--- Final Answer ---")
# print(response["output"])



import os
from crewai import Agent,Task,Crew,LLM
from crewai_tools import(
     WebsiteSearchTool,
     ScrapeWebsiteTool,
     TavilySearchTool
    )
from langchain_ollama import ChatOllama
# os.getenv["OPENAI_API_KEY"]="NA"
searchtool=TavilySearchTool()
scaping=ScrapeWebsiteTool()
llm = LLM(
    model="ollama/llama3.2", 
    temperature=0.3,
    base_url="http://localhost:11434" # Optional: guarantees mapping to local Ollama instance
)

urls_collecting= Agent(
    role="URL_Collector",
    goal="your goal is to collect the best and high clicked and popular websites urls based on the topic of user",
    backstory="you are a specialized URL collector your work is to collect the best suitable top urls," \
    " based on the topic provided by the user",
    tools=[searchtool],
    verbose=True,
    llm=llm
)

agent_Task=Task(
    description="collect a top 5 urls based on the topic of Generative AI",
    expected_output="collect the list of urls",
    agent=urls_collecting
)

crew=Crew(
    agents=[urls_collecting],
    tasks=[agent_Task],
    memory=False
)

result=crew.kickoff()
                                                                    