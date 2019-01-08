import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

LOG = get_logger('rest', 'rest.log')

class Rainbow6Siege(API):
    ID = 'RAINBOW6SIEGE'

    r6s_url = 'https://api.r6stats.com/api/v1'
    platforms = ['ps4', 'xone', 'uplay']

    # In this case unofficial denotes the fact that I'm hitting unofficial routes
    # The data itself is legit
    r6s_unofficial_url = 'https://r6stats.com/api'
    unofficial_platforms = ['ps4', 'xone', 'pc']
    unofficial_regions = ['all', 'ncsa', 'emea', 'apac']

    # For some reason the get calls for the official url are slow, the unofficial is a lot faster
    def _get(self, player, platform='uplay', operators = False):
        req_url = '{}/{}/{}'.format(self.r6s_url, 'players', player)

        if operators:
            req_url = '{}/operators?platform={}'.format(req_url, platform)
        else:
            req_url = '{}?platform={}'.format(req_url, platform)

        resp = requests.get(req_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()


    def _get_unofficial(self, uri):
        req_url = '{}/{}'.format(self.r6s_unofficial_url, uri)

        resp = requests.get(req_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()


    def get_player_info(self, player, platform=None):
        return self._get(player, platform=platform)


    def get_player_operators(self, player, platform=None):
        return self._get(player, platform=platform, operators=True)

    def get_leaderboards(self, platform='pc', region='all', page=1):
        return self._get_unofficial(
            'leaderboards/seasonal/{}/{}?page={}'.format(platform, region, page)
        )

    def get_player_stats(self, player_id):
        '''
        The player id in this case is a guid you can get from the get_leaderboards call
        You can also get this id from get_high_level_player_status ubisoft id
        '''

        return self._get_unofficial(
            'stats/{}'.format(player_id)
        )

    def get_player_stats_seasonal(self, player_id):
        '''
        The player id in this case is a guid you can get from the get_leaderboards call
        You can also get this id from get_high_level_player_status ubisoft id
        '''

        return self._get_unofficial(
            'stats/{}/seasonal'.format(player_id)
        )


    def get_high_level_player_status(self, player_name, platform='pc'):
        return self._get_unofficial(
            'player-search/{}/{}'.format(player_name, platform)
        )
