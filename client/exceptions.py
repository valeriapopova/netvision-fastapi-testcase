from requests.models import Response


def process_response(response: Response):
    try:
        return response.json()
    except:
        return response.content


class ConnectionFailure(Exception):
    def __init__(self, url: str):
        super().__init__(f'URL: {url}')


class BadResponse(Exception):
    def __init__(self, response: Response, body: dict | list = None):
        self.resp = process_response(response)
        super().__init__(f'response: {self.resp}; body: {body}')
