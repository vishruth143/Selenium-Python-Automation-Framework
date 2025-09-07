# pylint: disable=[unused-argument, missing-module-docstring, missing-module-docstring, unspecified-encoding]
# pylint: disable=[missing-function-docstring, line-too-long, import-outside-toplevel, deprecated-argument]
# pylint: disable=[broad-exception-caught]

import os
import shutil
import stat

def _on_rm_error(func, path, exc_info):
    # Try to remove read-only or locked files
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        print(f"Could not delete locked file: {path}")

# Clean up output folder before any tests run
def pytest_sessionstart(session):
    output_dir = os.path.join(os.getcwd(), 'output')
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir, onerror=_on_rm_error)
            print(f"Cleaned up output directory: {output_dir}")
        except Exception as e:
            print(f"Failed to clean output directory {output_dir}: {e}")
    else:
        print(f"Output directory does not exist, no cleanup needed: {output_dir}")

    # Create all required output subdirectories
    os.makedirs(os.path.join(output_dir, 'allure-results'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'reports'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'screenshots'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'videos'), exist_ok=True)

    env_file_path = os.path.join(output_dir, 'allure-results', 'environment.properties')
    with open(env_file_path, 'w') as f:
        f.write(f"REGION={os.getenv('REGION', 'QA')}")
        f.write(f"\nBROWSER={os.getenv('BROWSER', 'CHROME')}")
        f.write(f"\nHEADLESS={os.getenv('HEADLESS', 'N')}")
