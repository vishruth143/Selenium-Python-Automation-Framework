# pylint: disable=[unused-argument, missing-module-docstring, missing-module-docstring, unspecified-encoding]
# pylint: disable=[missing-function-docstring]

import os

def pytest_sessionstart(session):
    results_dir = os.path.join(os.getcwd(), 'output/allure-results')
    os.makedirs(results_dir, exist_ok=True)

    env_file_path = os.path.join(results_dir, 'environment.properties')
    with open(env_file_path, 'w') as f:
        f.write(f"REGION={os.getenv('REGION', 'undefined')}\n")
        f.write(f"BROWSER={os.getenv('BROWSER', 'undefined')}\n")
        f.write(f"HEADLESS={os.getenv('HEADLESS', 'undefined')}\n")

# During test collection, this code filters out any test not marked with the given APP_NAME or SERVICE_NAME
def pytest_collection_modifyitems(config, items):
    app_name = os.environ.get("APP_NAME", "").lower()
    service_name = os.environ.get("SERVICE_NAME", "").lower()

    selected_items = []

    for item in items:
        item_markers = {mark.name.lower() for mark in item.iter_markers()}

        if app_name and app_name in item_markers:
            selected_items.append(item)
        elif service_name and service_name in item_markers:
            selected_items.append(item)

    if app_name or service_name:
        items[:] = selected_items