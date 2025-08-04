# pylint: disable=[line-too-long, missing-module-docstring, missing-function-docstring]


import os
import re
from datetime import datetime


def get_project_root(project_name="Selenium-Python-Automation-Framework") -> str:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.basename(current_dir) == project_name:
            return current_dir
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            raise FileNotFoundError(f"Project root '{project_name}' not found.")
        current_dir = parent

def get_screenshot_path(test_name: str, subdir="screenshots") -> str:
    project_root = get_project_root()
    output_dir = os.path.join(project_root, "output", subdir)
    os.makedirs(output_dir, exist_ok=True)

    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', test_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{safe_name}_{timestamp}.png"

    return os.path.join(output_dir, file_name)
