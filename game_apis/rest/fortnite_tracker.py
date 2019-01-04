import requests
from game_apis.rest.api import API
from game_apis.log import get_logger

# https://documentation.pubg.com/en/getting-started.html
class FortniteTracker(API):
    ID = 'Fortnitetracker'
    LIMIT = 2

    def __init__(self, config, region=None, sandbox=False, local_config=False, ignore_limiter=False):
        super().__init__(config, sandbox, local_config, ignore_limiter)

        self.rest_api = "https://api.fortnitetracker.com/v1/"

    def _get(self, command: str, options = None):
        headers = {
            'TRN-Api-Key': self.key_id
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


    def player_stats(self, platform, epic_nickname):
        '''
        Parameters:
            platform: The platform you want fortnite player stats for. Current
                      options are: pc, xbl, psn

            epic_nickname: The nickname you use to log into epic games.

        returns a list of stats for the respective platform for the nickname.
        '''

        return self._get('/profile/{}/{}'.format(platform, epic_nickname))

    def matches(self, account_id):
        '''
        Parameters:
            account_id: The <accountId> parameter returned from the player_stats
                        function.

        returns a list of matches
        '''
        return self._get('/profile/account/{}/matches'.format(account_id))

    def get_store_info(self):
        '''
        Returns a list of items that represent what is currently in the fortnite store.
        '''
        return self._get('/store/')

    def get_challenges(self):
        '''
        Returns a list of current fortnite challenges.
        '''
        return self._get('/challenges')
