import os
import sys


def get_absolute_path(relative_path):
    """
    Get the absolute path to a file, works for both .py and .exe files.

    Args:
        relative_path (str): The relative path to the file.

    Returns:
        str: The absolute path to the file.
    """
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle (exe), use sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # If running as a script, use the directory of the current file
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Return the absolute path to the file
    return os.path.join(base_path, '..', relative_path)

def get_project_path():
    """Returns the absolute path to the project directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(filename):
    """Returns the path to the resource file."""
    return os.path.join(get_project_path(), filename)