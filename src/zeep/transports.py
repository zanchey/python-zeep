import requests

from zeep.cache import SqliteCache


class Transport(object):

    def __init__(self, cache=None, timeout=300, verify=True, http_auth=None):
        self.cache = cache or SqliteCache()
        self.timeout = timeout
        self.verify = verify
        self.http_auth = http_auth

        self.session = self.create_session()
        self.session.verify = verify
        self.session.auth = http_auth

    def create_session(self):
        return requests.Session()

    def load(self, url):
        if self.cache:
            response = self.cache.get(url)
            if response:
                return bytes(response)

        response = self.session.get(url, timeout=self.timeout)
        if self.cache:
            self.cache.add(url, response.content)

        return response.content

    def post(self, address, message, headers):
        response = self.session.post(address, data=message, headers=headers)
        return response

    def get(self, address, params, headers):
        response = self.session.get(address, params=params, headers=headers)
        return response
