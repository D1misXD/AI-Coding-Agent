import os

working_directory = os.path.abspath(".")

def get_files_info(directory="."):
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_directory.startswith(working_directory):
        return f'Error: "{directory}" is not in the working dir'
    
    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory,content)
        is_dir = os.path.isdir(os.path.join(abs_directory,content))
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size}, is_dir={is_dir}\n"
    return final_response