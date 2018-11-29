import unittest

from game_apis.rest import Rest

class TestPubg(unittest.TestCase):

    def test_region_default(self):
        pubg = Rest('config.yaml').Pubg
        assert pubg.rest_api == 'https://api.pubg.com/shards/pc-na'

    def test_region_different(self):
        pubg = Rest('config.yaml', region='test').Pubg
        assert pubg.rest_api == 'https://api.pubg.com/shards/test'

    def test_samples(self):
        pubg = Rest('config.yaml').Pubg
        samples = pubg.samples()

        assert len(samples) > 0
        assert samples['data']['relationships']['matches']['data'][0]['type'] == 'match'

    def test_get_players(self):
        pubg = Rest('config.yaml').Pubg
        players = pubg.get_players('playerNames', ['shroud'])

        assert len(players['data']) > 0

    def test_get_player(self):
        pubg = Rest('config.yaml').Pubg
        player = pubg.get_player('account.d50fdc18fcad49c691d38466bed6f8fd')
        assert player['data']['id'] == 'account.d50fdc18fcad49c691d38466bed6f8fd'

    def test_get_seasons(self):
        pubg = Rest('config.yaml').Pubg
        seasons = pubg.get_seasons()
        assert len(seasons['data']) > 0

    def test_get_player_season(self):
        pubg = Rest('config.yaml').Pubg
        season = pubg.get_player_season('account.d50fdc18fcad49c691d38466bed6f8fd', 'division.bro.official.pc-2018-01')
        assert season['data']['type'] == 'playerSeason'

    def test_get_match(self):
        pubg = Rest('config.yaml').Pubg
        player = pubg.get_player('account.d50fdc18fcad49c691d38466bed6f8fd')
        match = pubg.get_match(
            player['data']['relationships']['matches']['data'][0]['id']
        )

        assert 'data' in match

    def test_get_match_telemetry(self):
        pubg = Rest('config.yaml').Pubg
        player = pubg.get_player('account.d50fdc18fcad49c691d38466bed6f8fd')
        telemetry = pubg.get_match_telemetry(player['data']['relationships']['matches']['data'][0]['id'])

        assert len(telemetry) > 0

if __name__ == '__main__':
    unittest.main()
