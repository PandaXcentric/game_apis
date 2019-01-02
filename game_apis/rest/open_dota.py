import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

LOG = get_logger('rest', 'rest.log')

# https://docs.opendota.com
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

    def _post(self, command: str):
        if options is None:
            options = {}
        base_url = "{}{}".format(self.rest_api, command)

        if self.key_id is not None:
            base_url = "{}?api_key={}".format(base_url, self.key_id)

        resp = requests.post(base_url)

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

    def get_pro_players(self):
        return self._get('/proPlayers')

    # api to get player info
    def refresh_player(self, account_id):
        return self._post('/players/{}/refresh'.format(account_id))

    def _get_player(self, account_id, command = None, parameters = None):
        call = '/players/{}'.format(account_id)
        if command is not None:
            call = '{}/{}'.format(call, command)

        return self._get(call, parameters)

    def get_player_info(self, account_id):
        return self._get_player(account_id)

    def get_player_wl(self, account_id):
        return self._get_player(account_id, 'wl')

    def get_player_recent_matches(self, account_id):
        return self._get_player(account_id, 'recentMatches')

    def get_player_matches(self, account_id, parameters = None):
        '''
        account_id: account to get the matches for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1matches%2Fget
        '''
        return self._get_player(account_id, 'matches', parameters)

    def get_player_heroes(self, account_id, parameters = None):
        '''
        account_id: account to get the heroes for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1heroes%2Fget
        '''
        return self._get_player(account_id, 'heroes', parameters)

    def get_player_peers(self, account_id, parameters = None):
        '''
        account_id: account to get the people played with for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1peers%2Fget
        '''
        return self._get_player(account_id, 'peers', parameters)

    def get_pros_played_with(self, account_id, parameters = None):
        '''
        account_id: account to get the pros played with for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1pros%2Fget
        '''
        return self._get_player(account_id, 'pros', parameters)

    def get_player_totals(self, account_id, parameters = None):
        '''
        account_id: account to get the totals for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1totals%2Fget
        '''
        return self._get_player(account_id, 'totals', parameters)

    def get_player_counts(self, account_id, parameters = None):
        '''
        account_id: account to get the count for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1counts%2Fget
        '''
        return self._get_player(account_id, 'counts', parameters)

    def get_player_histogram(self, account_id, field, parameters = None):
        '''
        account_id: account to get the histogram for
        field: field to aggregate on
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1histograms~1%7Bfield%7D%2Fget
        '''
        call = '/players/{}/histograms/{}'.format(account_id, field)
        return self._get(call, parameters)

    def get_player_wardmap(self, account_id, parameters = None):
        '''
        account_id: account to get the wardmap for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1wardmap%2Fget
        '''
        return self._get_player(account_id, 'wardmap', parameters)

    def get_player_wordcloud(self, account_id, parameters = None):
        '''
        account_id: account to get the wardmap for
        Parameters:
            Accepted parameters can be found at https://docs.opendota.com/#tag/players%2Fpaths%2F~1players~1%7Baccount_id%7D~1wordcloud%2Fget
        '''
        return self._get_player(account_id, 'wordcloud')

    def get_player_ratings(self, account_id):
        return self._get_player(account_id, 'ratings')

    def get_player_rankings(self, account_id):
        return self._get_player(account_id, 'rankings')

    def get_pro_matches(self):
        return self._get('/proMatches')

    def get_public_matches(self, parameters = None):
        '''
        mmr_ascending: integer, Order by MMR ascending
        mmr_descending: integer, Order by MMR descending
        less_than_match_id: integer, Get matches with a match ID lower than this value
        '''
        return self._get('/publicMatches', parameters)

    def get_match(self, match_id):
        '''
        Parameters:
            match_id: integer match id to get
        '''
        return self._get('/matches/{}'.format(match_id))

    def search(self, query):
        return self._get('/search', query)

    def get_rankings(self, hero_id):
        '''
        Top players by hero
        '''
        return self._get('/rankings?hero_id={}'.format(hero_id))

    def get_benchmarks(self, hero_id):
        '''
        Benchmarks of average stat values for a hero
        '''
        return self._get('/benchmarks?hero_id={}'.format(hero_id))

    # api to get hero info
    def get_heroes(self):
        return self._get('/heroes')

    def get_hero_matches(self, hero_id):
        '''
        Get recent matches with a hero
        '''
        return self._get('/heroes/{}/matches'.format(hero_id))

    def get_hero_matchups(self, hero_id):
        '''
        Get results against other heroes for a hero
        '''
        return self._get('/heroes/{}/matchups'.format(hero_id))

    def get_hero_performance_durations(self, hero_id):
        '''
        Get hero performance over a range of match durations
        '''
        return self._get('/heroes/{}/durations'.format(hero_id))

    def get_hero_players(self, hero_id):
        '''
        Get players who have played this hero
        '''
        return self._get('/heroes/{}/players'.format(hero_id))

    def get_hero_stats(self):
        return self._get('/heroStats')

    def get_leagues(self):
        return self._get('/leagues')


    # api to get team info
    def get_teams(self):
        return self._get('/teams')

    def get_team_info(self, team_id):
        return self._get('/teams/{}'.format(team_id))

    def get_team_matches(self, team_id):
        return self._get('/teams/{}/matches'.format(team_id))

    def get_team_players(self, team_id):
        return self._get('/teams/{}/players'.format(team_id))

    def get_team_heroes(self, team_id):
        return self._get('/teams/{}/heroes'.format(team_id))

    def get_records(self, field):
        return self._get('/records/{}'.format(field))


    def get_live(self):
        return self._get('/live')
