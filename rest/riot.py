import requests
from rest.api import API
from log import get_logger

LOG = get_logger('rest', 'rest.log')

# https://developer.riotgames.com/api-methods/
class Riot(API):
    ID = 'RIOT'

    # potentially allow the region to be passed as an argument
    rest_api = "https://na1.api.riotgames.com/lol"

    def _get(self, command: str, options = None):
        if options is None:
            options = {}
        base_url = "{}{}".format(self.rest_api, command)

        if self.key_id is not None:
            base_url = "{}?api_key={}".format(base_url, self.key_id)

        # loop over dictionary of options and add them as query parameters to the url
        # example: currencyPair=BTC_NXT&depth=10
        for key, val in options.items():
            if "?" not in base_url:
                base_url = "{}?{}={}".format(base_url, key, val)
                continue

            base_url = "{}&{}={}".format(base_url, key, val)

        resp = requests.get(base_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()

    def hello_world(self):
        return self._get("/summoner/v3/summoners/by-name/RiotSchmick")
