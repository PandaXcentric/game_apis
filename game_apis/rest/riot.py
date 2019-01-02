import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

LOG = get_logger('rest', 'rest.log')

# https://developer.riotgames.com/api-methods/
class Riot(API):
    ID = 'RIOT'
    LIMIT = 1

    def __init__(self, config, region=None, sandbox=False, local_config=False, ignore_limiter=False):
        super().__init__(config, sandbox, local_config, ignore_limiter)

        if region == None:
            region = 'na1'

        self.rest_api = "https://{}.api.riotgames.com".format(region)


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

        self.check_limiter()

        resp = requests.get(base_url)

        self.reset_limiter()

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()

    def hello_world(self):
        return self._get("/lol/summoner/v3/summoners/by-name/RiotSchmick")

    def champion_masteries(self, summoner_id):
        return self._get('/lol/champion-mastery/v3/champion-masteries/by-summoner/{}'.format(summoner_id))

    def champion_mastery(self, summoner_id, champoin_id):
        return self._get('/lol/champion-mastery/v3/champion-masteries/by-summoner/{}/by-champion/{}'.format(summoner_id, champoin_id))

    def champion_mastery_score(self, summoner_id):
        return self._get('/lol/champion-mastery/v3/scores/by-summoner/{}'.format(summoner_id))

    def champion_rotations(self):
        return self._get('/lol/platform/v3/champion-rotations')

    # api to get summoner information
    def get_summoner_by_account(self, account_id):
        return self._get('/lol/summoner/v3/summoners/by-account/{}'.format(account_id))

    def get_summoner_by_name(self, summoner_name):
        return self._get('/lol/summoner/v3/summoners/by-name/{}'.format(summoner_name))

    def get_summoner_by_summoner_id(self, summoner_id):
        return self._get('/lol/summoner/v3/summoners/{}'.format(summoner_id))

    def get_matches_for_account(self, account_id, parameters = None):
        return self._get('/lol/match/v3/matchlists/by-account/{}'.format(account_id), parameters)


    def get_match_by_id(self, match_id):
        return self._get('/lol/match/v3/matches/{}'.format(match_id))

    def get_match_timeline(self, match_id):
        return self._get('/lol/match/v3/timelines/by-match/{}'.format(match_id))

    def get_match_ids_tournament(self, tournament_code):
        return self._get(' /lol/match/v3/matches/by-tournament-code/{}/ids'.format(tournament_code))

    def get_current_game_info(self, summoner_id):
        return self._get('/lol/spectator/v3/active-games/by-summoner/{}'.format(summoner_id))

    def get_featured_games(self):
        return self._get('/lol/spectator/v3/featured-games')
