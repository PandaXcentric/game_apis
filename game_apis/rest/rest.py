import logging

from game_apis.rest.open_dota import OpenDota
from game_apis.rest.riot import Riot
from game_apis.rest.pubg import Pubg

class Rest:
    def __init__(self, config=None, sandbox=False, local_config=False):
        self.config = config
        self.lookup = {
            'opendota': OpenDota(config,sandbox,local_config),
            'riot': Riot(config,sandbox,local_config),
            'pubg': Pubg(config,sandbox,local_config)
        }

    def __getattr__(self, attr):
        return self.lookup[attr.lower()]
