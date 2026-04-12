# pylint: disable=[unused-argument, missing-module-docstring, missing-module-docstring, unspecified-encoding]
# pylint: disable=[missing-function-docstring, line-too-long, import-outside-toplevel, deprecated-argument]
# pylint: disable=[broad-exception-caught]

import os
import shutil
import stat
import logging

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
