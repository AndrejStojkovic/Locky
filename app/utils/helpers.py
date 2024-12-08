import os

def get_project_path():
    """Returns the absolute path to the project directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(filename):
    """Returns the path to the resource file."""
    return os.path.join(get_project_path(), filename)