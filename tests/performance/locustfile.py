# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring]
# pylint: disable=[line-too-long, duplicate-code]

"""
JSONPlaceholder Performance Test Suite — Locust
================================================
Target  : https://jsonplaceholder.typicode.com
Run     : see README "Running Performance Tests" section

User behaviour modelled:
  JsonPlaceholderUser  — realistic read/write mix simulating a client
                         that browses posts, reads comments, fetches
                         users, creates posts, updates & deletes them.

Task weights reflect a realistic traffic distribution:
  GET (read) operations are far more common than writes.

  Weight  Task
  ------  -------------------------------------------------
  10      GET /posts                 (list all posts)
  8       GET /posts/{id}            (read a single post)
  6       GET /posts/{id}/comments   (read comments for a post)
  6       GET /users                 (list all users)
  4       GET /users/{id}/todos      (read todos for a user)
  3       POST /posts                (create a new post)
  2       PUT /posts/{id}            (fully replace a post)
  2       PATCH /posts/{id}          (partially update a post)
  1       DELETE /posts/{id}         (delete a post)
"""

import os
import random

import yaml
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner, WorkerRunner


# ---------------------------------------------------------------------------
# Load performance config
# ---------------------------------------------------------------------------
_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..",
    "config", "performance", "jsonplaceholder", "perf_test_config.yml")

with open(os.path.normpath(_CONFIG_PATH), encoding="utf-8") as _f:
    _ALL_CONFIG = yaml.safe_load(_f)

_REGION = os.environ.get("REGION", "QA").upper()
_CONFIG = _ALL_CONFIG.get(_REGION, _ALL_CONFIG["QA"])


# ---------------------------------------------------------------------------
# JsonPlaceholderUser
# ---------------------------------------------------------------------------
class JsonPlaceholderUser(HttpUser):
    """
    Simulates a user interacting with the JSONPlaceholder REST API.

    Think time (wait_time) is randomised between think_time_min and
    think_time_max seconds (read from config) to model realistic
    user pacing and avoid thundering-herd patterns.
    """

    wait_time = between(
        _CONFIG.get("think_time_min", 1),
        _CONFIG.get("think_time_max", 3),
    )

    # ── Shared test-data constants ──────────────────────────────────────────
    # JSONPlaceholder has 100 posts and 10 users — stay within bounds.
    _POST_IDS = list(range(1, 101))
    _USER_IDS = list(range(1, 11))

    _CREATE_PAYLOAD = {
        "title": "performance test post",
        "body": "created by locust performance test",
        "userId": 1,
    }

    _UPDATE_PAYLOAD = {
        "id": 1,
        "title": "updated by performance test",
        "body": "full replacement via PUT",
        "userId": 1,
    }

    _PATCH_PAYLOAD = {"title": "patched by performance test"}

    # ── READ tasks (high frequency) ─────────────────────────────────────────

    @task(10)
    def get_all_posts(self):
        """GET /posts — list all 100 posts (most common read operation)."""
        self.client.get("/posts", name="GET /posts")

    @task(8)
    def get_single_post(self):
        """GET /posts/{id} — fetch one post by random ID."""
        post_id = random.choice(self._POST_IDS)
        self.client.get(f"/posts/{post_id}", name="GET /posts/{id}")

    @task(6)
    def get_post_comments(self):
        """GET /posts/{id}/comments — fetch comments for a random post."""
        post_id = random.choice(self._POST_IDS)
        self.client.get(
            f"/posts/{post_id}/comments",
            name="GET /posts/{id}/comments",
        )

    @task(6)
    def get_all_users(self):
        """GET /users — list all 10 users."""
        self.client.get("/users", name="GET /users")

    @task(4)
    def get_user_todos(self):
        """GET /users/{id}/todos — fetch all items for a random user."""
        user_id = random.choice(self._USER_IDS)
        self.client.get(f"/users/{user_id}/todos", name="GET /users/{id}/todos")

    # ── WRITE tasks (low frequency) ─────────────────────────────────────────

    @task(3)
    def create_post(self):
        """POST /posts — create a new post (simulated, not persisted)."""
        self.client.post(
            "/posts",
            json=self._CREATE_PAYLOAD,
            name="POST /posts",
        )

    @task(2)
    def update_post(self):
        """PUT /posts/{id} — fully replace a random post."""
        post_id = random.choice(self._POST_IDS)
        payload = {**self._UPDATE_PAYLOAD, "id": post_id}
        self.client.put(
            f"/posts/{post_id}",
            json=payload,
            name="PUT /posts/{id}",
        )

    @task(2)
    def patch_post(self):
        """PATCH /posts/{id} — partial update on a random post."""
        post_id = random.choice(self._POST_IDS)
        self.client.patch(
            f"/posts/{post_id}",
            json=self._PATCH_PAYLOAD,
            name="PATCH /posts/{id}",
        )

    @task(1)
    def delete_post(self):
        """DELETE /posts/{id} — delete a random post (simulated)."""
        post_id = random.choice(self._POST_IDS)
        self.client.delete(
            f"/posts/{post_id}",
            name="DELETE /posts/{id}",
        )


# ---------------------------------------------------------------------------
# Locust event hooks
# ---------------------------------------------------------------------------

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Print the active config at startup so it's visible in the console."""
    if not isinstance(environment.runner, (MasterRunner, WorkerRunner)):
        print(
            f"\n{'='*60}\n"
            f"  JSONPlaceholder Performance Test\n"
            f"  Region  : {_REGION}\n"
            f"  Host    : {_CONFIG.get('base_url')}\n"
            f"  Users   : {_CONFIG.get('users')}\n"
            f"  Rate    : {_CONFIG.get('spawn_rate')} users/sec\n"
            f"  Runtime : {_CONFIG.get('run_time')}\n"
            f"{'='*60}\n"
        )


@events.request.add_listener
def on_request(request_type, name, response_time, response_length,
               response, context, exception, **kwargs):
    """
    Log every failed request to stdout for quick debugging.
    Response time is in milliseconds.
    """
    if exception:
        print(
            f"[FAIL] {request_type} {name} | "
            f"time={response_time:.0f}ms | error={exception}"
        )
    elif response and response.status_code >= 400:
        print(
            f"[FAIL] {request_type} {name} | "
            f"status={response.status_code} | time={response_time:.0f}ms"
        )

