import logging

from rest.open_dota import OpenDota

class Rest:
    def __init__(self, config=None, sandbox=False):
        self.config = config
        self.lookup = {
            'opendota': OpenDota(config)
        }

    def __getattr__(self, attr):
        return self.lookup[attr.lower()]
