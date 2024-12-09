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
        # If running as a script, use the directory of the main script (app.py)
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, relative_path)

def get_project_path():
    """Returns the absolute path to the project directory."""
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle (exe), use sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # If running as a script, use the directory of the main script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return base_path

def get_resource_path(filename):
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
        # If running as a script, use the directory of the main script
        base_path = os.path.dirname(os.path.abspath(__file__))  # Use __file__ for proper reference

    absolute_path = os.path.join(base_path, filename)
    return absolute_path