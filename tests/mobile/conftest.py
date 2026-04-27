# pylint: disable = [line-too-long, missing-module-docstring, missing-function-docstring]
# =============================================================================
# MOBILE CONFTEST - shared scaffolding for all mobile test suites
# =============================================================================
#
# This file is auto-loaded by pytest for every test under tests/mobile/.
# It owns ONLY truly cross-app concerns (the Appium server lifecycle).
#
# App-specific fixtures (testdata, driver / desired capabilities, app launch)
# live in per-app conftests:
#   tests/mobile/kwa/conftest.py    - KWA fixtures
#
# Add cross-app helpers here only if they are reused by more than one mobile
# app suite.
# =============================================================================
import pytest
from appium.webdriver.appium_service import AppiumService
@pytest.fixture(scope="session", autouse=True)
def appium_server():
    """Start a local Appium server for the duration of the test session."""
    print('-' * 10 + ' Starting Appium Server ' + '-' * 10)
    appium_service = AppiumService()
    appium_service.start()
    print(f"Appium service is running? - {appium_service.is_running}")
    print(f"Appium service is listening? - {appium_service.is_listening}")
    if not appium_service.is_running:
        raise RuntimeError("Appium server failed to start.")
    yield appium_service
    print('-' * 10 + ' Stopping Appium Server ' + '-' * 10)
    appium_service.stop()
    print(f"Appium service is running? - {appium_service.is_running}")
    print(f"Appium service is listening? - {appium_service.is_listening}")
