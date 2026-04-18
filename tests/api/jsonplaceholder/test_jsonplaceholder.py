# pylint: disable=[duplicate-code, line-too-long, attribute-defined-outside-init, missing-module-docstring]
# pylint: disable=[no-else-continue, invalid-name, logging-fstring-interpolation, import-error]
# pylint: disable=[too-many-statements, too-many-branches, unused-variable, too-many-locals, unsubscriptable-object]
# pylint: disable=C0302

import pytest

from config.config_parser import ConfigParser
from framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])
jsonplaceholder_api_test_data = ConfigParser.load_config("jsonplaceholder_api_test_data_config")


@pytest.mark.jsonplaceholder
class TestJsonPlaceholder:

    """
    Test cases for JSONPlaceholder API (https://jsonplaceholder.typicode.com)
    A free, registration-free fake REST API for testing and prototyping.
    Resources: /posts, /comments, /albums, /photos, /todos, /users
    """

    def test_get_posts(self, api_client):
        """
        Test #01 : Verify GET /posts returns a list of posts.
        Steps:
        01) Send GET request to /posts.
        02) Verify status code is 200.
        03) Verify response is a non-empty list.
        04) Verify each post has the expected fields: id, title, body, userId.
        """
        endpoint = "/posts"

        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify GET /posts returns a list of posts.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to /posts.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify response is a non-empty list.")
            posts = response.json()
            assert isinstance(posts, list), f"Expected a list, got {type(posts)}"
            assert len(posts) > 0, "Expected at least one post in the response."
            log.info(f"Response contains {len(posts)} post(s).")

            log.info("STEP 04: Verify each post contains the expected fields.")
            required_fields = {"id", "title", "body", "userId"}
            for post in posts:
                missing = required_fields - post.keys()
                assert not missing, f"Post ID {post.get('id')} is missing fields: {missing}"
            log.info("All posts contain the expected fields: id, title, body, userId.")

            log.info("Test #01 : Verify GET /posts - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #01 : Verify GET /posts - Failed")
            raise

    def test_get_single_post(self, api_client):
        """
        Test #02 : Verify GET /posts/1 returns the correct post.
        Steps:
        01) Send GET request to /posts/1.
        02) Verify status code is 200.
        03) Verify post ID is 1 and userId is 1.
        04) Verify title and body fields are non-empty strings.
        """
        endpoint = "/posts/1"

        try:
            log.info(50 * '*')
            log.info("Test #02 : Verify GET /posts/1 returns the correct post.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to /posts/1.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify post ID is 1 and userId is 1.")
            post = response.json()
            assert post["id"] == 1, f"Expected id=1, got {post.get('id')}"
            assert post["userId"] == 1, f"Expected userId=1, got {post.get('userId')}"
            log.info(f"Post ID and userId verified: id={post['id']}, userId={post['userId']}")

            log.info("STEP 04: Verify title and body are non-empty strings.")
            assert isinstance(post["title"], str) and post["title"], "Expected non-empty title string."
            assert isinstance(post["body"], str) and post["body"], "Expected non-empty body string."
            log.info(f"Title: '{post['title']}' | Body (truncated): '{post['body'][:50]}...'")

            log.info("Test #02 : Verify GET /posts/1 - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #02 : Verify GET /posts/1 - Failed")
            raise

    def test_create_post(self, api_client):
        """
        Test #03 : Verify POST /posts creates a new post.
        Steps:
        01) Send POST request to /posts with test data payload.
        02) Verify status code is 201.
        03) Verify the response echoes back title, body, and userId.
        04) Verify the response contains a new 'id' field.
        """
        endpoint = "/posts"
        payload = jsonplaceholder_api_test_data.get("CreatePost", {})

        try:
            log.info(50 * '*')
            log.info("Test #03 : Verify POST /posts creates a new post.")
            log.info(50 * '*')

            log.info(f"STEP 01: Sending POST request to /posts with payload: {payload}")
            response = api_client.post(endpoint, json=payload)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code is 201.")
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            log.info("Status code is 201 as expected.")

            log.info("STEP 03: Verify the response echoes back title, body, and userId.")
            data = response.json()
            assert data["title"] == payload["title"], f"Expected title '{payload['title']}', got '{data.get('title')}'"
            assert data["body"] == payload["body"], f"Expected body '{payload['body']}', got '{data.get('body')}'"
            assert data["userId"] == payload["userId"], f"Expected userId {payload['userId']}, got {data.get('userId')}"
            log.info("Response body matches the sent payload.")

            log.info("STEP 04: Verify response contains a new 'id' field.")
            assert "id" in data, "Expected 'id' field in the creation response."
            log.info(f"New post created with id: {data['id']}")

            log.info("Test #03 : Verify POST /posts - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #03 : Verify POST /posts - Failed")
            raise

    def test_update_post(self, api_client):
        """
        Test #04 : Verify PUT /posts/1 fully updates a post.
        Steps:
        01) Send PUT request to /posts/1 with a full update payload.
        02) Verify status code is 200.
        03) Verify all updated fields are reflected in the response.
        """
        endpoint = "/posts/1"
        payload = jsonplaceholder_api_test_data.get("UpdatePost", {})

        try:
            log.info(50 * '*')
            log.info("Test #04 : Verify PUT /posts/1 fully updates a post.")
            log.info(50 * '*')

            log.info(f"STEP 01: Sending PUT request to /posts/1 with payload: {payload}")
            response = api_client.put(endpoint, json=payload)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify all updated fields are reflected in the response.")
            data = response.json()
            assert data["id"] == payload["id"], f"Expected id={payload['id']}, got {data.get('id')}"
            assert data["title"] == payload["title"], f"Expected title '{payload['title']}', got '{data.get('title')}'"
            assert data["body"] == payload["body"], f"Expected body '{payload['body']}', got '{data.get('body')}'"
            assert data["userId"] == payload["userId"], f"Expected userId={payload['userId']}, got {data.get('userId')}"
            log.info("All updated fields verified in the response.")

            log.info("Test #04 : Verify PUT /posts/1 - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #04 : Verify PUT /posts/1 - Failed")
            raise

    def test_patch_post(self, api_client):
        """
        Test #05 : Verify PATCH /posts/1 partially updates a post.
        Steps:
        01) Send PATCH request to /posts/1 with a partial payload (title only).
        02) Verify status code is 200.
        03) Verify the patched field is updated in the response.
        """
        endpoint = "/posts/1"
        payload = jsonplaceholder_api_test_data.get("PatchPost", {})

        try:
            log.info(50 * '*')
            log.info("Test #05 : Verify PATCH /posts/1 partially updates a post.")
            log.info(50 * '*')

            log.info(f"STEP 01: Sending PATCH request to /posts/1 with payload: {payload}")
            response = api_client.patch(endpoint, json=payload)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify the patched title field is updated in the response.")
            data = response.json()
            assert data["title"] == payload["title"], (
                f"Expected title '{payload['title']}', got '{data.get('title')}'"
            )
            log.info(f"Patched title verified: '{data['title']}'")

            log.info("Test #05 : Verify PATCH /posts/1 - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #05 : Verify PATCH /posts/1 - Failed")
            raise

    def test_delete_post(self, api_client):
        """
        Test #06 : Verify DELETE /posts/1 deletes a post.
        Steps:
        01) Send DELETE request to /posts/1.
        02) Verify status code is 200.
        03) Verify the response body is an empty JSON object {}.
        """
        endpoint = "/posts/1"

        try:
            log.info(50 * '*')
            log.info("Test #06 : Verify DELETE /posts/1 deletes a post.")
            log.info(50 * '*')

            log.info("STEP 01: Sending DELETE request to /posts/1.")
            response = api_client.delete(endpoint)
            log.info(f"Response received: {response.status_code}")
            log.info(f"Response body: {response.text}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify the response body is an empty JSON object.")
            data = response.json()
            assert data == {}, f"Expected empty object {{}}, got {data}"
            log.info("Response body is an empty JSON object as expected.")

            log.info("Test #06 : Verify DELETE /posts/1 - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #06 : Verify DELETE /posts/1 - Failed")
            raise

    def test_get_post_comments(self, api_client):
        """
        Test #07 : Verify GET /posts/1/comments returns comments for post 1.
        Steps:
        01) Send GET request to /posts/1/comments.
        02) Verify status code is 200.
        03) Verify response is a non-empty list.
        04) Verify each comment has: id, postId, name, email, body fields.
        05) Verify all comments belong to postId 1.
        """
        endpoint = "/posts/1/comments"

        try:
            log.info(50 * '*')
            log.info("Test #07 : Verify GET /posts/1/comments returns comments for post 1.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to /posts/1/comments.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify response is a non-empty list.")
            comments = response.json()
            assert isinstance(comments, list), f"Expected a list, got {type(comments)}"
            assert len(comments) > 0, "Expected at least one comment."
            log.info(f"Response contains {len(comments)} comment(s).")

            log.info("STEP 04: Verify each comment has required fields.")
            required_fields = {"id", "postId", "name", "email", "body"}
            for comment in comments:
                missing = required_fields - comment.keys()
                assert not missing, f"Comment ID {comment.get('id')} is missing fields: {missing}"
            log.info("All comments contain the expected fields.")

            log.info("STEP 05: Verify all comments belong to postId 1.")
            for comment in comments:
                assert comment["postId"] == 1, (
                    f"Comment ID {comment.get('id')} has postId={comment.get('postId')}, expected 1."
                )
            log.info("All comments are associated with postId 1 as expected.")

            log.info("Test #07 : Verify GET /posts/1/comments - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #07 : Verify GET /posts/1/comments - Failed")
            raise

    def test_get_users(self, api_client):
        """
        Test #08 : Verify GET /users returns a list of users.
        Steps:
        01) Send GET request to /users.
        02) Verify status code is 200.
        03) Verify response contains exactly 10 users.
        04) Verify each user has: id, name, username, email, address, phone, website, company.
        """
        endpoint = "/users"

        try:
            log.info(50 * '*')
            log.info("Test #08 : Verify GET /users returns a list of users.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to /users.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify response contains exactly 10 users.")
            users = response.json()
            assert isinstance(users, list), f"Expected a list, got {type(users)}"
            assert len(users) == 10, f"Expected 10 users, got {len(users)}"
            log.info(f"Response contains {len(users)} user(s) as expected.")

            log.info("STEP 04: Verify each user has the expected top-level fields.")
            required_fields = {"id", "name", "username", "email", "address", "phone", "website", "company"}
            for user in users:
                missing = required_fields - user.keys()
                assert not missing, f"User ID {user.get('id')} is missing fields: {missing}"
            log.info("All users contain the expected fields.")

            log.info("Test #08 : Verify GET /users - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #08 : Verify GET /users - Failed")
            raise

    def test_get_todos_by_user(self, api_client):
        """
        Test #09 : Verify GET /users/1/todos returns todos for user 1.
        Steps:
        01) Send GET request to /users/1/todos.
        02) Verify status code is 200.
        03) Verify response is a non-empty list.
        04) Verify each item has: id, userId, title, completed fields.
        05) Verify all todos belong to userId 1.
        """
        endpoint = "/users/1/todos"

        try:
            log.info(50 * '*')
            log.info("Test #09 : Verify GET /users/1/todos returns todos for user 1.")
            log.info(50 * '*')

            log.info("STEP 01: Sending GET request to /users/1/todos.")
            response = api_client.get(endpoint)
            log.info(f"Response received: {response.status_code}")

            log.info("STEP 02: Validating status code is 200.")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            log.info("Status code is 200 as expected.")

            log.info("STEP 03: Verify response is a non-empty list.")
            todos = response.json()
            assert isinstance(todos, list), f"Expected a list, got {type(todos)}"
            assert len(todos) > 0, "Expected at least one item in the response."
            log.info(f"Response contains {len(todos)} item(s).")

            log.info("STEP 04: Verify each item has required fields.")
            required_fields = {"id", "userId", "title", "completed"}
            for todo_item in todos:
                missing = required_fields - todo_item.keys()
                assert not missing, f"Item ID {todo_item.get('id')} is missing fields: {missing}"
            log.info("All todos contain the expected fields: id, userId, title, completed.")

            log.info("STEP 05: Verify all todos belong to userId 1.")
            for todo_item in todos:
                assert todo_item["userId"] == 1, (
                    f"Item ID {todo_item.get('id')} has userId={todo_item.get('userId')}, expected 1."
                )
            log.info("All todos are associated with userId 1 as expected.")

            log.info("Test #09 : Verify GET /users/1/todos - Completed Successfully.")

        except Exception as e:
            log.error(f"Exception occurred: {e}")
            log.info("Test #09 : Verify GET /users/1/todos - Failed")
            raise
