import requests
from rest.api import API
from log import get_logger

LOG = get_logger('rest', 'rest.log')

class OpenDota(API):
    '''
    OpenDota integrates with the OpenDota api.
    '''
    ID = 'OPENDOTA'

    rest_api = "https://api.opendota.com/api"

    def _get(self, command: str, options = None):
        if options is None:
            options = {}
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

    # scenarios apis
    def get_item_timings(self, parameters = None):
        '''
        Paramenters:
            item: item name (replace space with underscore, e.g. "spirit_vessel")
            hero_id: id of hero

        If no parameters are passed, get_scenarios returns all combinations of hero and item.
        '''
        return self._get('/scenarios/itemTimings', parameters)

    def get_lane_roles(self, parameters = None):
        '''
        Parameters:
            lane_role: Filter by lane role 1-4 (Safe, Mid, Off, Jungle)
            hero_id: id of hero

        If no parameters are passed get all combinations
        If both parameters are passed, get list of results that are win rates by time slice. e.g. [{'hero_id': 62, 'lane_role': 1, 'time': 900, 'games': '394', 'wins': '201'}, {'hero_id': 62, 'lane_role': 1, 'time': 1800, 'games': '4586', 'wins': '1926'}, ...]
        '''
        return self._get('/scenarios/laneRoles', parameters)

    def get_misc_scenarios(self, parameters = None):
        '''
        Parameters:
            scenario: pos_chat_1min,neg_chat_1min,courier_kill,first_blood

        if a scenario is passed, returns a list of win rate for each region
        '''
        return self._get('/scenarios/misc', parameters)
