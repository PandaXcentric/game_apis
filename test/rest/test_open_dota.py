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

        assert len(scenarios) == 1

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

if __name__ == '__main__':
    unittest.main()
