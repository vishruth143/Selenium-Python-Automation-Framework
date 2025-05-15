import os

def pytest_sessionstart(session):
    results_dir = os.path.join(os.getcwd(), 'allure-results')
    os.makedirs(results_dir, exist_ok=True)

    env_file_path = os.path.join(results_dir, 'environment.properties')
    with open(env_file_path, 'w') as f:
        f.write(f"REGION={os.getenv('REGION', 'undefined')}\n")
        f.write(f"BROWSER={os.getenv('BROWSER', 'undefined')}\n")
        f.write(f"HEADLESS={os.getenv('HEADLESS', 'undefined')}\n")