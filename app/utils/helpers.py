import os
import sys
from pathlib import Path

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
    """Returns the path to the resource file relative to the project directory."""
    project_path = get_project_path()
    resource_path = os.path.join(project_path, filename)
    if not os.path.isfile(resource_path):
        print(f"Error: Resource file not found at {resource_path}")
    return resource_path

def get_database_path():
    """
    Returns the absolute path to the locky_db.db file.
    - If running from source: places the database in the root folder.
    - If running as a standalone executable: places the database in a writable directory.
    """
    if getattr(sys, 'frozen', False):  # Running as an .exe
        # Use a writable directory (e.g., APPDATA/Locky)
        base_path = Path(os.getenv('APPDATA')) / "Locky"
    else:  # Running from source
        # Use the script's root directory
        base_path = Path(os.path.dirname(os.path.abspath(__file__)))

    # Ensure the base directory exists
    base_path.mkdir(parents=True, exist_ok=True)

    return base_path / "locky_db.db"