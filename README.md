# AI Coding Agent

A command-line coding agent built with **LangChain**, **LangGraph** and **Google Gemini 2.5 Flash**.
You describe a programming task in plain language, and the agent decides on its own which tools to use:
it can list and read files, write code, run Python scripts and search the web for documentation,
repeating these steps until the task is done.

The project was developed as part of the undergraduate thesis
*"Ευφυείς πράκτορες στην τεχνολογία λογισμικού"* (Intelligent Agents in Software Engineering),
Department of Informatics, Democritus University of Thrace, 2026.

---

## Features

- **Natural-language tasks** – ask for a new program, a new feature or a bug fix in plain English or Greek.
- **Tool use** – the agent chooses between five tools and chains them as needed (e.g. read → write → run).
- **Session memory** – follow-up requests in the same session remember earlier files, answers and tool results.
- **Live trace** – every tool call and its result are printed in the terminal, followed by the final answer and the execution time.
- **Safety limits** – file access is restricted to the working directory, scripts time out after 30 seconds, and the number of reasoning steps per request is capped.

## How it works

```
You ──► CLI (main.py) ──► Gemini 2.5 Flash ──► needs a tool? ──yes──► run tool ──► result back to the model ─┐
                                   ▲                  │                                                     │
                                   │                  no                                                    │
                                   │                  ▼                                                     │
                                   │            final answer ──► printed in the terminal                    │
                                   └────────────────────────────────────────────────────────────────────────┘
```

1. Your request is sent to the model together with the system prompt and the session history.
2. The model either answers directly or calls one of the tools.
3. The tool's output is added to the conversation, and the model decides the next step.
4. The loop repeats until the model gives a final answer, or until the step limit (`recursion_limit = 10`) is reached.

The agent is created with LangChain's `create_agent()`. LangGraph runs the loop, and `MemorySaver` keeps the conversation state in memory.

## Tools

| Tool | What it does | Limits |
|---|---|---|
| `get_files_info_tool` | Lists the files and folders in a directory, with size and type | Working directory only |
| `get_files_content_tool` | Reads a file's contents | Working directory only; up to `MAX_CHARS` (10,000) characters |
| `write_file_tool` | Creates or overwrites a file, creating parent folders if needed | Working directory only |
| `run_python_file_tool` | Runs a `.py` file and returns STDOUT, STDERR and the exit code | `.py` files only; 30-second timeout |
| `search_web_tool` | Searches the web with Tavily (up to 5 results) | The system prompt asks for at most 2 searches per session |

## Project structure

```
AI-Coding-Agent/
├── main.py                  # Entry point: model, agent, memory and the CLI loop
├── config.py                # Settings (MAX_CHARS)
├── requirements.txt         # Python dependencies
├── functions/
│   ├── wrappers.py          # Wraps the functions below as LangChain tools (@tool)
│   ├── get_files_info.py    # List directory contents
│   ├── get_files_content.py # Read a file
│   ├── write_file.py        # Write / overwrite a file
│   ├── run_python_file.py   # Run a Python file in a subprocess
│   └── search_web.py        # Tavily web search
├── machine.txt              # Sample file for testing the read tool
└── nice_day.txt             # Sample file for testing the read tool
```

## Requirements

- **Python 3.12** (other 3.10+ versions should also work)
- A **Google Gemini API key** – free from [Google AI Studio](https://aistudio.google.com/apikey)
- A **Tavily API key** – free tier available at [tavily.com](https://tavily.com) (needed for web search)

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/AI-Coding-Agent.git
cd AI-Coding-Agent
```

**2. Create and activate a virtual environment**

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install the dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your API keys**

Create a file named `.env` in the project folder (next to `main.py`):

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> ⚠️ Never commit the `.env` file. Add `.env` to your `.gitignore` so your keys stay private.

## Usage

Run the agent **from the project folder**:

```bash
python main.py
```

Type a request after `You:` and press Enter. Type `exit` or `quit` to stop.

### Example

```
You: Read nice_day.txt and tell me what it says

--------------------------------------------------
TOOL USED
--------------------------------------------------
Name: get_files_content_tool

--------------------------------------------------
TOOL RESULT
--------------------------------------------------
Have a nice day!

==================================================
AGENT RESPONSE
==================================================

The file nice_day.txt says: "Have a nice day!"

Execution time: 2.41 seconds
```

### More things to try

- `Create a Snake game in snake.py using Pygame, with random obstacles.`
- `Read snake.py and add a restart option after Game Over.`
- `Run calculator.py and fix any errors you find.`
- `Search the Pygame documentation for KEYDOWN and improve the keyboard handling in snake.py.`

Tip: for debugging, ask the agent to **read** the code, not just run it. A program can run without errors and still contain a logic bug.

## Configuration

| Setting | Where | Default | Meaning |
|---|---|---|---|
| `MAX_CHARS` | `config.py` | `10000` | Maximum characters returned when reading a file |
| `model` | `main.py` | `gemini-2.5-flash` | The Gemini model used |
| `recursion_limit` | `main.py` | `10` | Maximum internal steps per request; raise it for longer tasks |
| `thread_id` | `main.py` | `session-1` | Identifies the conversation for memory |
| `timeout` | `functions/run_python_file.py` | `30` seconds | Maximum running time of a script |

## Limitations

- **The working directory is the folder you run `main.py` from.** The agent can read and overwrite any file there, including its own source code, so it's best to give it tasks on separate files.
- **Not a full sandbox.** Scripts run as normal processes on your computer; only the path checks and the timeout limit them.
- **Interactive programs time out.** Games or GUIs keep running until closed, so `run_python_file_tool` stops them after 30 seconds. That is expected, not an error. Test them yourself by running them directly.
- **Memory is temporary.** The conversation is kept in RAM and is lost when the program exits.
- **The web search limit is advisory.** The 2-searches rule is in the prompt, not enforced in code.
- **Results can vary.** The model may choose different steps for similar requests, so always review the code it writes.

## Built with

- [LangChain](https://docs.langchain.com/oss/python/langchain/agents) – agent and tool framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) – execution loop and memory (`MemorySaver`)
- [Google Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/models) via `langchain-google-genai`
- [Tavily](https://tavily.com) via `langchain-tavily` – web search
- [python-dotenv](https://pypi.org/project/python-dotenv/) – loading API keys from `.env`
- [Pydantic](https://docs.pydantic.dev/) – tool argument schemas

