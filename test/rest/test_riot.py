import unittest

import rest
from rest import rest
from rest.rest import Rest

class TestRiot(unittest.TestCase):

    def test_hello_world(self):
        riot = Rest('config.yaml').Riot
        hello = riot.hello_world()

        assert hello['id'] == 585897

    def test_champion_masteries(self):
        riot = Rest('config.yaml').Riot
        summoner = riot.get_summoner_by_name('pandaxcentric')
        champions = riot.champion_masteries(summoner['id'])
        assert len(champions) >= 0


    def test_champoin_mastery_score(self):
        riot = Rest('config.yaml').Riot
        summoner = riot.get_summoner_by_name('pandaxcentric')
        mastery = riot.champoin_mastery_score(summoner['id'])
        assert mastery >= 0

    def test_champoin_rotations(self):
        riot = Rest('config.yaml').Riot
        rotations = riot.champoin_rotations()

        assert len(rotations['freeChampionIds']) > 0

    def test_get_summoner_by_name(self):
        riot = Rest('config.yaml').Riot
        summoner = riot.get_summoner_by_name('pandaxcentric')
        assert 'id' in summoner

    def test_get_matches_for_account(self):
        riot = Rest('config.yaml').Riot
        summoner = riot.get_summoner_by_name('pandaxcentric')
        matches = riot.get_matches_for_account(summoner['accountId'])

        assert len(matches['matches']) > 0

    def test_get_match_timeline(self):
        riot = Rest('config.yaml').Riot

        summoner = riot.get_summoner_by_name('pandaxcentric')
        matches = riot.get_matches_for_account(summoner['accountId'])

        timeline = riot.get_match_timeline(matches['matches'][0]['gameId'])

        assert timeline['frameInterval'] > 0

    def test_get_featured_games(self):
        riot = Rest('config.yaml').Riot
        featured = riot.get_featured_games()
        assert len(featured['gameList']) > 0


if __name__ == '__main__':
    unittest.main()
