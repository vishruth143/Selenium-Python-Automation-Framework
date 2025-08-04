# pylint: disable=[line-too-long, missing-module-docstring, missing-function-docstring]


import os
import re
from datetime import datetime

def get_screenshot_path(test_name: str, subdir="screenshots") -> str:
    # Go up three levels from this file's directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_dir = os.path.join(project_root, "output", subdir)
    os.makedirs(output_dir, exist_ok=True)

    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', test_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{safe_name}_{timestamp}.png"

    return os.path.join(output_dir, file_name)
