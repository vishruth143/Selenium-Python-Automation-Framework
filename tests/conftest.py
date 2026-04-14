# pylint: disable=[unused-argument, missing-module-docstring, missing-module-docstring, unspecified-encoding]
# pylint: disable=[missing-function-docstring, line-too-long, import-outside-toplevel, deprecated-argument]
# pylint: disable=[broad-exception-caught]

import os
import shutil
import stat
import logging
import json
import platform

def _on_rm_error(func, path, exc_info):
    # Try to remove read-only or locked files
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        print(f"Could not delete locked file: {path}")

def _release_log_handlers():
    """
    Close and remove every file handler attached to every active logger.
    This releases the OS-level lock on test_execution.log (and any other
    log files) so that shutil.rmtree can delete the output folder cleanly.
    The handlers are opened fresh once the output directories are recreated.
    """
    for name, logger in list(logging.Logger.manager.loggerDict.items()):
        if isinstance(logger, logging.Logger):
            for handler in list(logger.handlers):
                try:
                    handler.flush()
                    handler.close()
                except Exception:
                    pass
                logger.removeHandler(handler)

# Clean up output folder before any tests run
def pytest_sessionstart(session):
    # Release all open log file handles BEFORE attempting to delete the folder.
    # Logger instances created at module level (e.g. in test files) open
    # test_execution.log immediately on import, which locks the file on Windows.
    # Closing every handler here lets shutil.rmtree proceed without errors.
    _release_log_handlers()

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

    # Copy categories.json into allure-results so the Allure "Categories" tab
    # groups failures into meaningful buckets (Product Defects, Test Defects, etc.)
    categories_src = os.path.join(os.getcwd(), 'config', 'categories.json')
    categories_dst = os.path.join(output_dir, 'allure-results', 'categories.json')
    if os.path.exists(categories_src):
        shutil.copy2(categories_src, categories_dst)
        print(f"Copied categories.json to: {categories_dst}")

    # Generate executor.json so the Allure "Executors" widget shows
    # who/what ran the tests (CI server or local machine).
    executor_data = _build_executor_info()
    executor_path = os.path.join(output_dir, 'allure-results', 'executor.json')
    with open(executor_path, 'w') as f:
        json.dump(executor_data, f, indent=2)
    print(f"Generated executor.json: {executor_data.get('name')}")


def _build_executor_info():
    """
    Return an executor dict for Allure.
    Detects GitHub Actions, Jenkins, or falls back to local machine info.
    """
    # --- GitHub Actions ---
    if os.getenv('GITHUB_ACTIONS') == 'true':
        server_url = os.getenv('GITHUB_SERVER_URL', 'https://github.com')
        repo = os.getenv('GITHUB_REPOSITORY', '')
        run_id = os.getenv('GITHUB_RUN_ID', '')
        run_number = os.getenv('GITHUB_RUN_NUMBER', '0')
        build_url = f"{server_url}/{repo}/actions/runs/{run_id}"
        return {
            "name": "GitHub Actions",
            "type": "github",
            "buildName": f"Run #{run_number}",
            "buildUrl": build_url,
            "buildOrder": int(run_number),
            "reportUrl": build_url,
        }

    # --- Jenkins ---
    if os.getenv('JENKINS_URL'):
        return {
            "name": "Jenkins",
            "type": "jenkins",
            "buildName": os.getenv('BUILD_DISPLAY_NAME', os.getenv('BUILD_NUMBER', 'N/A')),
            "buildUrl": os.getenv('BUILD_URL', ''),
            "buildOrder": int(os.getenv('BUILD_NUMBER', '0')),
            "reportUrl": os.getenv('BUILD_URL', ''),
        }

    # --- Local machine ---
    return {
        "name": f"Local ({platform.node()})",
        "type": "local",
        "buildName": f"{platform.system()} {platform.release()}",
    }
