import time

from langchain_core.messages import ToolMessage, AIMessage
from agent import agent


def main():

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