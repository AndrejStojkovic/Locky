import os
import subprocess

# List of .py files in the project directory
project_root = os.path.dirname(os.path.abspath(__file__))
py_files = []

# Walk through the entire directory and subdirectories
for root, _, files in os.walk(project_root):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            py_files.append(f'"{file_path}"')  # Wrap path in quotes for Windows compatibility

# Join all file paths into a single string
py_files_str = ' '.join(py_files)

# Run the pylupdate5 command
try:
    command = f'pylupdate5 {py_files_str} -ts en.ts mk.ts'
    print(f"Running command: {command}\n")
    subprocess.run(command, shell=True, check=True)
    print("Translation files (en.ts, mk.ts) have been generated successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
