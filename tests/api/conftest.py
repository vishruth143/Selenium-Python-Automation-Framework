# pylint: disable=[missing-module-docstring, missing-function-docstring, line-too-long]
# =============================================================================
# API CONFTEST - shared scaffolding for all API test suites
# =============================================================================
#
# This file is intentionally kept minimal. Service-specific fixtures
# (api_client, testdata, auth tokens, etc.) live in per-service conftests:
#   tests/api/jsonplaceholder/conftest.py   - JSONPlaceholder fixtures
#
# Add cross-service helpers here only if they are reused by more than one
# service test suite.
# =============================================================================
