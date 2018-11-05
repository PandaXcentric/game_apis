import unittest

import rest
from rest import rest
from rest.rest import Rest

class TestOpenDota(unittest.TestCase):

    def test_get_live(self):
        dota = Rest('config.yaml').OpenDota
        live = dota.get_live()

        assert len(live) >= 0
        if len(live) > 0:
            assert len(live[0]['players']) > 0


if __name__ == '__main__':
    unittest.main()
