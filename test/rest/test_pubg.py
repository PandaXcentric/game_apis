import unittest

import rest
from rest import rest
from rest.rest import Rest

class TestPubg(unittest.TestCase):

    def test_samples(self):
        pubg = Rest('config.yaml').Pubg
        samples = pubg.samples()

        assert len(samples) > 0
        assert samples['data']['relationships']['matches']['data'][0]['type'] == 'match'

if __name__ == '__main__':
    unittest.main()
