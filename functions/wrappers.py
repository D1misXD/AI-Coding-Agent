from langchain_core.tools import tool
from functions.get_files_info import get_files_info as get_files_info_fn
from functions.get_files_content import get_file_content as get_file_content_fn
from functions.run_python_file import run_python_file as run_python_fn
from functions.write_file import write_file as write_file_fn
from functions.search_web import search_tool as search_file_fn
import os
from pydantic import BaseModel

WORKING_DIRECTORY = os.path.abspath(".")

class RunArgs(BaseModel):
    file_path: str
    args: list[str] = []

@tool
def get_files_info_tool(directory: str = ".") -> str:
    """Get info about files in a directory"""
    return get_files_info_fn(directory)

@tool
def get_files_content_tool(file_path: str) -> str:
    """Read a file's content"""
    return get_file_content_fn(file_path)

@tool(args_schema=RunArgs)
def run_python_file_tool(file_path: str, args = []) -> str:
    """Run a python file with the python interpreter. Accepts additional CLI args as an optional array."""
    return run_python_fn(file_path, args)

@tool
def write_file_tool(file_path: str, content: str) -> str:
    """Overwrites an existing file or writes a new file if it doesn't exist (and created required parent dirs safely),constrainted to the working directory
    """
    return write_file_fn(file_path, content)

@tool
def search_web_tool(quary: str) -> str:
    """Search the web for programming documentation, API usage,
    coding examples, and error explanations.
    Use this when local project files are insufficient.
    Prefer official documentation and primary sources whenever possible.
    When searching for a library, framework, language, or API, formulate
    the query so that official documentation is prioritized.
    You have a limit of 2 searches per session.
    """
    return search_file_fn(quary)