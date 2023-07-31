import random
import json
import time
import requests
import string

import exceptions
from logger import CustomLogger


API_URL = 'http://0.0.0.0:8000'


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return {"text": rand_string}


def generate_random_strings():
    num_strings = random.randint(10, 100)
    strings_list = [generate_random_string(16) for _ in range(num_strings)]
    return strings_list


class Client:
    def __init__(self, logger: CustomLogger):
        self.log = logger
        self.api_url = API_URL
        self.deleted_entries = 0

    def create_entries(self):
        method_url = '/new'
        _url = self.api_url + method_url
        _data = generate_random_strings()

        try:
            resp = requests.post(
                url=_url,
                json=json.dumps(_data),
            )
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout
        ) as error:
            raise exceptions.ConnectionFailure(_url) from error
        return resp

    def get_entries(self):
        method_url = '/10'
        _url = self.api_url + method_url

        try:
            resp = requests.get(
                url=_url
            )
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout
        ) as error:
            raise exceptions.ConnectionFailure(_url) from error
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if resp.status_code == 404:
                raise exceptions.BadResponse(resp) from error
        if resp.json():
            entries_uuids = [r['uuid'] for r in resp.json()]

            self.delete_entries(entries_uuids)
        else:
            return 0

    def delete_entries(self, entries_uuids: list):
        for uuid in entries_uuids:
            method_url = f'/{uuid}'
            _url = self.api_url + method_url
            try:
                resp = requests.delete(
                    url=_url
                )
            except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout
            ) as error:
                raise exceptions.ConnectionFailure(_url) from error

            try:
                resp.raise_for_status()
                self.deleted_entries += 1
                return self.deleted_entries
            except requests.exceptions.HTTPError as error:
                if resp.status_code == 404:
                    raise exceptions.BadResponse(resp) from error

    def run(self):
        self.create_entries()
        while True:
            time.sleep(10)
            entries = self.get_entries()
            if entries:
                log.evt.info(f'{entries} entries was deleted')
            else:
                log.evt.info(f'no entries found')
                break


if __name__ == "__main__":
    log = CustomLogger()

    log.evt.info('client app started')

    client = Client(log)
    client.run()

    log.evt.info(f'script finished')
