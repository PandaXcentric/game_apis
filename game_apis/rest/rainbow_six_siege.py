import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

LOG = get_logger('rest', 'rest.log')

class Rainbow6Siege(API):
    ID = 'RAINBOW6SIEGE'

    r6s_url = 'https://api.r6stats.com/api/v1'
    platforms = ['ps4', 'xone', 'uplay']

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


    def get_player_info(self, player, platform=None):
        return self._get(player, platform=platform)


    def get_player_operators(self, player, platform=None):
        return self._get(player, platform=platform, operators=True)
