import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        # Add the API key header here
        self.session.headers.update({
            "x-api-key": "reqres-free-v1"
        })

    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, data=None, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def put(self, endpoint: str, data=None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)