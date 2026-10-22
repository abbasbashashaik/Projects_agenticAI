from langchain_ollama import ChatOllama
from crewai import Crew,Agent,Task,Process,LLM
from app.schemas import ResumeEvaluation


def ask_llm(job_description:str,resume_txt:str):
    local_llm = LLM(
        model="ollama/llama3.2",
        base_url="http://localhost:11434"
    )

    analysis_agent=Agent(
        role="Senior Resume Screener",
        goal="Accurately evaluate resumes against job requirements and identify gaps.",
        backstory="You are a seasoned HR professional with 10+ years of technical recruiting experience.",
        verbose=False,                # Prints internal thoughts and logic to terminal
        memory=False,                 # Allows agent to remember across task executions
        allow_delegation=False,  
                 # Prevents this agent from passing tasks to others
        llm=local_llm
        
                             # Assigns your Ollama or OpenAI model
        )
    writer_agent = Agent(
        role="Executive HR Copywriter",
        goal="Transform structured JSON data into professional, executive-ready narrative reports.",
        backstory="You excel at explaining technical metrics and talent gaps using fluent corporate sentences.",
        verbose=False,
        llm=local_llm
    )
    screening_task = Task(
        description=f"Compare the candidate resume: {resume_txt} with the job description: {job_description}.",
        expected_output="A structured report containing overall profile score with compared to job description and, key missing skills, and a final recommendation.",
        agent=analysis_agent,
        #output_pydantic=ResumeEvaluation,               # The Agent assigned to execute this task
        output_file="screening_report.json"  # Automatically writes the final text output to a file
    )
    report_generation_task = Task(
        description=(
            "Take the structured JSON evaluation data from the previous task. "
            "Convert it into a professional, human-readable report. "
            "You MUST use clear Markdown headings and write out the explanations "
            "using detailed full sentences. Do not just print raw JSON values."
        ),
        expected_output="A beautiful Markdown report with Headings and detailed narrative explanations.",
        agent=writer_agent,
        output_file="final_screening_report.md"  # Saves as a markdown text file in your project folder
    )
    hr_crew =Crew(
        agents=[analysis_agent,writer_agent],
        tasks=[screening_task,report_generation_task],
        process=Process.sequential,
        verbose=True
        
    )
    result= hr_crew.kickoff(
       inputs= {
            "resume":resume_txt,
            "jd":job_description
        }
    )
    return {"result":result.raw}