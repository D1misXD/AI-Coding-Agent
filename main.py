import time

from dotenv import load_dotenv
import os
from langchain_core.messages import ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from functions.wrappers import (
    get_files_info_tool,
    get_files_content_tool,
    run_python_file_tool,
    write_file_tool,
    search_web_tool
)

def main():
        
    load_dotenv()

    tools = [
             get_files_info_tool,
             get_files_content_tool,
             run_python_file_tool,
             write_file_tool,
             search_web_tool]
    
    system_prompt = ("""
You are a coding agent.

You can:
- List files
- Read files
- Write/overwrite files
- Run Python scripts
- You can search the web when needed, but you have a limit of 2 searches per session.

Always use tools when needed.
All paths are relative to the working directory.
""")
    memory = MemorySaver()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        api_version="v1beta"
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=memory
    )

    config = {
    "configurable": {
        "thread_id": "session-1"
    },
    "recursion_limit": 10
    }

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        final_message = None

        start_time = time.perf_counter()

        for update in agent.stream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                },
                config=config,
                stream_mode="updates"
        ):

            for node_data in update.values():
                messages = node_data.get("messages", [])

                for message in messages:

                    if isinstance(message, AIMessage):

                        for tool_call in message.tool_calls:
                            print("\n" + "-" * 50)
                            print("TOOL USED")
                            print("-" * 50)
                            print(f"Name: {tool_call['name']}")

                        if message.content:
                            final_message = message

                    elif isinstance(message, ToolMessage):
                        print("\n" + "-" * 50)
                        print("TOOL RESULT")
                        print("-" * 50)
                        print(message.content)

        print("\n" + "=" * 50)
        print("AGENT RESPONSE")
        print("=" * 50 + "\n")

        if final_message is not None:

            if isinstance(final_message.content, str):
                print(final_message.content)

            else:
                print(final_message.content[0]["text"])

        end_time = time.perf_counter()

        execution_time = end_time - start_time
        print(f"\nExecution time: {execution_time:.2f} seconds")

        print("\n" + "=" * 50)

main()