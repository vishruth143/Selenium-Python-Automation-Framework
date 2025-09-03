import requests
from requests.auth import HTTPBasicAuth

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.session = requests.Session()

        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, data=None, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def put(self, endpoint: str, data=None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    def get_oauth_token(self, auth_url, client_id, client_secret):
        """Obtain OAuth2 access token using client_credentials flow."""
        token_url = f"{auth_url}/oauth/token"

        response = self.session.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(client_id, client_secret)
        )
        '''
        If the response status code is 400–599 (client or server error), it raises a requests.exceptions.HTTPError.
        If the response status code is 200–299 (success), it does nothing and execution continues.
        '''
        response.raise_for_status()

        json_data = response.json()

        # Assert token_type is 'Bearer'
        assert json_data.get("token_type") == "Bearer", (
            f"Expected token_type 'Bearer', but got {json_data.get('token_type')}"
        )

        # Assert expires_in is greater than 0
        expires_in = json_data.get("expires_in", 0)
        assert isinstance(expires_in, int) and expires_in > 0, (
            f"Expected expires_in > 0, but got {expires_in}"
        )

        # Assert access_token is not missing or empty
        token = json_data.get("access_token")
        assert token, "Access token is missing or empty"

        return token