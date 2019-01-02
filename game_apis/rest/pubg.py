import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

LOG = get_logger('rest', 'rest.log')

# https://documentation.pubg.com/en/getting-started.html
class Pubg(API):
    ID = 'PUBG'
    LIMIT = 6 # rate limit of 10 requests per minute.

    def __init__(self, config, region=None, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        if region == None:
            region = 'pc-na'

        self.rest_api = "https://api.pubg.com/shards/{}".format(region)

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

        self.check_limiter()
        resp = requests.get(base_url, headers = headers)
        self.reset_limiter()

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

    def get_players(self, filter, players):
        '''
        filter: either playerIds or playerNames
        players: list of string, pass either ids or names depending on the filter
        '''
        return self._get('/players?filter[{}]={}'.format(filter, ",".join(players)))

    def get_player(self, account_id):
        '''
        account_id: account to get the info for
        '''
        return self._get('/players/{}'.format(account_id))

    def get_seasons(self):
        return self._get('/seasons')

    def get_player_season(self, account_id, season_id):
        return self._get('/players/{}/seasons/{}'.format(account_id, season_id))

    def get_lifetime_stats(self, account_id):
        return self._get('/players/{}/seasons/lifetime'.format(account_id))

    def get_match(self, id):
        return self._get('/matches/{}'.format(id))

    def get_match_telemetry(self, id):
        telemetry = None
        match = self.get_match(id)
        for info in match['included']:
            if info['type'] == 'asset':
                resp = requests.get(
                    info['attributes']['URL'],
                    headers = {'Accept': 'application/vnd.api+json', 'Accept-Encoding': 'gzip'}
                )
                telemetry = resp.json()

        return telemetry
