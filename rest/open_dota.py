import requests
from rest.api import API

class OpenDota(API):
    '''
    OpenDota integrates with the OpenDota api.
    '''
    ID = 'OPENDOTA'

    rest_api = "https://api.opendota.com/api"

    def _get(self, command: str, options = {}):
        base_url = "{}{}".format(self.rest_api, command)

        if self.key_id is not None:
            base_url = "{}?api_key={}".format(base_url, val)

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


    def get_live(self):
        '''
        Returns top currently ongoing live games
        '''
        return self._get('/live')
