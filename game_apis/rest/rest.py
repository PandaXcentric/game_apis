import logging

from game_apis.rest.open_dota import OpenDota
from game_apis.rest.riot import Riot
from game_apis.rest.riot_esports import RiotEsports
from game_apis.rest.pubg import Pubg
from game_apis.rest.fortnite_tracker import FortniteTracker

class Rest:
    def __init__(self, config=None, region=None, sandbox=False, local_config=False, ignore_limiter=False):
        self.config = config
        self.lookup = {
            'opendota': OpenDota(config,sandbox,local_config,ignore_limiter),
            'riot': Riot(config,region,sandbox,local_config,ignore_limiter),
            'riotesports': RiotEsports(config,sandbox,local_config,ignore_limiter),
            'pubg': Pubg(config,region,sandbox,local_config,ignore_limiter),
            'fortnitetracker': FortniteTracker(config,region,sandbox,local_config,ignore_limiter)
        }

    def __getattr__(self, attr):
        return self.lookup[attr.lower()]
