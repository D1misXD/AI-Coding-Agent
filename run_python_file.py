import os
import subprocess

working_directory = os.path.abspath(".")

def run_python_file(file_path: str, args = []):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(working_directory):
        return f'Error: "{file_path}" is not in the working dir'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        final_args = ["D:\\AI Agent LLM Project\\venv\\Scripts\\python.exe", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args, 
            cwd = working_directory, 
            timeout=30,
            capture_output=True
            ) 
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr} 
"""
        if final_string == ""  and output.stderr == "":
            final_string = "No output produced.\n"
        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
        return final_string
    except Exception as e:
        return f'Error: executing Python file: {e}'