import requests
from rest.api import API
from log import get_logger

LOG = get_logger('rest', 'rest.log')

# https://documentation.pubg.com/en/getting-started.html
class Pubg(API):
    ID = 'PUBG'

    rest_api = 'https://api.pubg.com/shards/pc-na'

    def _get(self, command: str, options = None):
        headers = {
            'Authorization': 'Bearer {}'.format(self.key_id),
            'Accept': 'application/vnd.api+json'
        }

        if options is None:
            options = {}
        base_url = "{}{}".format(self.rest_api, command)

        # loop over dictionary of options and add them as query parameters to the url
        # example: currencyPair=BTC_NXT&depth=10
        for key, val in options.items():
            if "?" not in base_url:
                base_url = "{}?{}={}".format(base_url, key, val)
                continue

            base_url = "{}&{}={}".format(base_url, key, val)

        resp = requests.get(base_url, headers = headers)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()


    def samples(self, parameters = None):
        '''
        Parameters:
            filter: The starting search date in UTC (Default now - 24 hours)

        returns a list of matches that can be used to infer trends in pubg
        The list is located in resp_data['data']['relationships']['matches']['data']
        '''
        return self._get('/samples', parameters)
