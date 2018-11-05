import logging

from rest.open_dota import OpenDota
from rest.riot import Riot
from rest.pubg import Pubg

class Rest:
    def __init__(self, config=None, sandbox=False):
        self.config = config
        self.lookup = {
            'opendota': OpenDota(config),
            'riot': Riot(config),
            'pubg': Pubg(config)
        }

    def __getattr__(self, attr):
        return self.lookup[attr.lower()]
