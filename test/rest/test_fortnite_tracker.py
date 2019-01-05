import unittest

from game_apis.rest import Rest

class TestFortniteTracker(unittest.TestCase):

    def test_default_url(self):
        fortnite = Rest('config.yaml', ignore_limiter=True).FortniteTracker
        assert fortnite.rest_api == 'https://api.fortnitetracker.com/v1/'

    def test_get_player_stats(self):
        fortnite = Rest('config.yaml', ignore_limiter=True).FortniteTracker
        player_stats = fortnite.get_player_stats('pc', 'ninja')

        assert len(player_stats['accountId']) > 0

    def test_get_matches(self):
        fortnite = Rest('config.yaml', ignore_limiter=True).FortniteTracker
        matches = fortnite.get_matches('4735ce91-3292-4caf-8a5b-17789b40f79c')
        assert len(matches) >= 0

    def test_get_store_info(self):
        fortnite = Rest('config.yaml', ignore_limiter=True).FortniteTracker
        store_info = fortnite.get_store_info()
        assert len(store_info) > 0

    def test_get_challenges(self):
        fortnite = Rest('config.yaml', ignore_limiter=True).FortniteTracker
        challenges = fortnite.get_challenges()
        assert len(challenges) > 0

if __name__ == '__main__':
    unittest.main()
