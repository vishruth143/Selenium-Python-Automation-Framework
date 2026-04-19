# pylint: disable=[missing-module-docstring, missing-function-docstring, import-error, redefined-outer-name]

import os
import pytest
import pandas as pd
import requests

from config.config_parser import ConfigParser

# REST Countries free tier allows max 10 fields per request.
# Split across two calls and merge on cca3.
_FIELDS_PRIMARY = "name,cca2,cca3,region,subregion,population,flags,latlng,borders,timezones"
_FIELDS_SECONDARY = "cca3,currencies,area"


@pytest.fixture(scope="session")
def data_config():
    """Load data validation config for the current region."""
    region = os.environ.get("REGION", "QA").upper()
    config = ConfigParser.load_config("restcountries_data_validation_config")
    return config.get(region, config["QA"])


def _fetch(base_url: str, fields: str) -> list:
    """Helper: GET /all with a specific fields list; assert 200."""
    url = f"{base_url}/all?fields={fields}"
    response = requests.get(url, timeout=30)
    assert response.status_code == 200, (
        f"GET {url} returned {response.status_code}: {response.text[:200]}"
    )
    return response.json()


@pytest.fixture(scope="session")
def all_countries(data_config):
    """
    Fetch all countries in two batches (max 10 fields each) and merge on cca3.
    The result is a list of dicts containing all required fields.
    """
    base = data_config["base_url"]

    primary = {c["cca3"]: c for c in _fetch(base, _FIELDS_PRIMARY) if "cca3" in c}
    secondary = {c["cca3"]: c for c in _fetch(base, _FIELDS_SECONDARY) if "cca3" in c}

    # Merge secondary fields into primary records
    for cca3, extra in secondary.items():
        if cca3 in primary:
            primary[cca3].update(extra)

    return list(primary.values())


@pytest.fixture(scope="session")
def countries_df(all_countries):
    """
    Flatten the merged country list into a pandas DataFrame.
    Exposes key scalar fields for aggregate / statistical analysis.
    """
    rows = []
    for country in all_countries:
        rows.append({
            "name":       country.get("name", {}).get("common", ""),
            "cca2":       country.get("cca2", ""),
            "cca3":       country.get("cca3", ""),
            "region":     country.get("region", ""),
            "subregion":  country.get("subregion", ""),
            "population": country.get("population", 0),
            "area":       country.get("area"),
            "borders":    country.get("borders", []),
            "timezones":  country.get("timezones", []),
            "currencies": list(country.get("currencies", {}).keys()),
        })
    return pd.DataFrame(rows)
