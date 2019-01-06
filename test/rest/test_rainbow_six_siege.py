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

        print(info)
        assert len(info['operator_records']) > 0
