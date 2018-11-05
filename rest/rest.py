import logging

from rest.open_dota import OpenDota
from rest.riot import Riot

class Rest:
    def __init__(self, config=None, sandbox=False):
        self.config = config
        self.lookup = {
            'opendota': OpenDota(config),
            'riot': Riot(config)
        }

    def __getattr__(self, attr):
        return self.lookup[attr.lower()]
