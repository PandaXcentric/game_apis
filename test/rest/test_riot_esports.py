import unittest

from game_apis.rest import Rest

class TestRiotEsports(unittest.TestCase):

    def test_leagues(self):
        esports = Rest('config.yaml').RiotEsports
        leagues = esports.leagues()

        assert len(leagues) > 0
        assert 'slug' in leagues[0]

    def test_league_info(self):
        esports = Rest('config.yaml').RiotEsports
        info = esports.league_info('lck')

        assert 'highlanderTournaments' in info

    def test_get_games_in_timeframe(self):
        esports = Rest('config.yaml').RiotEsports
        games = esports.get_games_in_timeframe('lck', 1499801019810, 1499801039810)

        assert len(games) > 0
        assert 'id' in games[0]

    def test_scheduled_items(self):
        esports = Rest('config.yaml').RiotEsports
        items = esports.scheduled_items(6)

        assert 'scheduleItems' in items
        assert len(items['scheduleItems']) > 0

    def test_scheduled_items_timeframe(self):
        esports = Rest('config.yaml').RiotEsports
        items = esports.scheduled_items_timeframe(6, 1499801019810, 1499801039810)

        assert len(items) > 0


    def test_match_details(self):
        esports = Rest('config.yaml').RiotEsports
        details = esports.match_details('0a5fb908-70c8-411b-81e0-27a83c167eda', '0be830cd-5583-4cb1-912b-bd635b7e2f0d')

        assert 'gameIdMappings' in details
        assert len(details['gameIdMappings']) > 0


    def test_game_stats(self):
        esports = Rest('config.yaml').RiotEsports
        stats = esports.game_stats('lck', 780772, '04eaa5d5cea58689')

        assert 'gameId' in stats

    def test_game_timeline(self):
        esports = Rest('config.yaml').RiotEsports
        timeline = esports.game_timeline('lck', 780772, '04eaa5d5cea58689')

        assert 'frames' in timeline


if __name__ == '__main__':
    unittest.main()
