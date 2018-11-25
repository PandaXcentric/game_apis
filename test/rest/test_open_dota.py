import unittest

from game_apis.rest import Rest

class TestOpenDota(unittest.TestCase):

    def test_get_live(self):
        dota = Rest('config.yaml').OpenDota
        live = dota.get_live()

        assert len(live) >= 0
        if len(live) > 0:
            assert len(live[0]['players']) > 0

    def test_get_item_timings(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_item_timings()

        assert len(scenarios) > 0

    def test_get_item_timings_item(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_item_timings({'item': 'ancient_janggo'})

        assert len(scenarios) > 0

    def test_get_item_timings_hero(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_item_timings({'hero_id': 120})

        assert len(scenarios) > 0

    def test_get_item_timings_both(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_item_timings({'hero_id': 120, 'item': 'ancient_janggo'})
        assert len(scenarios) > 1

    def test_get_lane_roles(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_lane_roles()

        assert len(scenarios) > 0

    def test_get_lane_roles_both(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_lane_roles({'hero_id': 62, 'lane_role': 1})

        assert len(scenarios) > 0


    def test_get_misc_scenarios(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_misc_scenarios()

        assert len(scenarios) > 0

    def test_get_misc_scenarios_param(self):
        dota = Rest('config.yaml').OpenDota
        scenarios = dota.get_misc_scenarios({'scenario': 'courier_kill'})

        assert len(scenarios) > 0

    def test_get_pro_players(self):
        dota = Rest('config.yaml').OpenDota
        pro_players = dota.get_pro_players()

        assert len(pro_players) > 0
        assert 'account_id' in pro_players[0]


    def test_get_match(self):
        dota = Rest('config.yaml').OpenDota
        match_id = dota.get_pro_matches()[0]['match_id']
        match = dota.get_match(match_id)

        assert match_id == match['match_id']

    def test_get_player_heroes(self):
        dota = Rest('config.yaml').OpenDota
        pro_players = dota.get_pro_players()
        player_heroes = dota.get_player_heroes(pro_players[0]['account_id'])

        assert len(player_heroes) > 0
        assert 'hero_id' in player_heroes[0]

    def test_get_player_heroes_parameters(self):
        dota = Rest('config.yaml').OpenDota
        pro_players = dota.get_pro_players()

        parameters = {
            'limit': 1,
            'offset': 1,
            'hero_id': 2
        }

        player_heroes = dota.get_player_heroes(pro_players[0]['account_id'], parameters)
        assert player_heroes[0]['games'] <= 1


    def test_get_player_wardmap(self):
        dota = Rest('config.yaml').OpenDota
        pro_players = dota.get_pro_players()
        wardmap = dota.get_player_wardmap(pro_players[0]['account_id'])
        assert 'obs' in wardmap

    def test_get_benchmarks(self):
        dota = Rest('config.yaml').OpenDota
        benchmark = dota.get_benchmarks(2)
        assert benchmark['hero_id'] == 2

    def test_get_hero_matchups(self):
        dota = Rest('config.yaml').OpenDota
        matchups = dota.get_hero_matchups(2)

        assert len(matchups) > 0

    def test_get_teams(self):
        dota = Rest('config.yaml').OpenDota
        teams = dota.get_teams()
        assert len(teams) > 0
        assert 'team_id' in teams[0]


    def test_get_team_matches(self):
        dota = Rest('config.yaml').OpenDota
        team = teams = dota.get_teams()[0]
        matches = dota.get_team_matches(team['team_id'])
        assert len(matches) > 0


if __name__ == '__main__':
    unittest.main()
