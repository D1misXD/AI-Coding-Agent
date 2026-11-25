from dotenv import load_dotenv
load_dotenv()

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from functions.wrappers import (
    get_files_info_tool,
    get_files_content_tool,
    run_python_file_tool,
    write_file_tool,
    search_web_tool,
)

SYSTEM_PROMPT = """
You are a coding agent.

You can:
- List files
- Read files
- Write/overwrite files
- Run Python scripts
- You can search the web when needed, but you have a limit of 2 searches per session.

Always use tools when needed.
All paths are relative to the working directory.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    api_version="v1beta",
)

agent = create_agent(
    model=llm,
    tools=[
        get_files_info_tool,
        get_files_content_tool,
        run_python_file_tool,
        write_file_tool,
        search_web_tool,
    ],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=MemorySaver(),
)