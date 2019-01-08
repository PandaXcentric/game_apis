import unittest

from game_apis.rest import Rest

class TestRainbow6Siege(unittest.TestCase):

    def test_get_player_info(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        info = r6s.get_player_info('barzY-YT', 'uplay')

        assert info['player']['username'] == 'barzY-YT'


    def test_get_player_operators(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        info = r6s.get_player_operators('barzY-YT', 'uplay')

        assert len(info['operator_records']) > 0


    def test_get_leaderboards(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        leaders = r6s.get_leaderboards('pc', page=1)

        assert len(leaders) == 100


    def test_get_player_stats_seasonal(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        player_stats = r6s.get_player_stats_seasonal('bedbbe83-015a-4e6f-babc-580c6e6ff9f3')

        assert player_stats['username'] == 'SanalsBae'


    def test_get_player_stats(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        player_stats = r6s.get_player_stats('bedbbe83-015a-4e6f-babc-580c6e6ff9f3')

        assert player_stats['username'] == 'SanalsBae'


    def test_get_high_level_player_status(self):
        r6s = Rest('config.yaml', ignore_limiter=True).Rainbow6Siege
        player_stats = r6s.get_high_level_player_status('SanalsBae', 'pc')

        assert player_stats[0]['ubisoft_id'] == 'bedbbe83-015a-4e6f-babc-580c6e6ff9f3'
