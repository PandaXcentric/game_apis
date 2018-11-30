import requests
from game_apis.rest.api import API
from game_apis.log import get_logger
from datetime import datetime
import time

LOG = get_logger('rest', 'rest.log')

class RiotEsports(API):
    ID = 'RIOTESPORTS'

    lolsports_rest_api = 'https://api.lolesports.com/api'
    leagueoflegends_rest_api = 'https://acs.leagueoflegends.com'
    ddragon_rest_api = 'https://ddragon.leagueoflegends.com'

    region_code_mapping = {
        'na-lcs': 'TRLH1',
        'lck': 'ESPORTSTMNT06',
        'lms': 'TRTW',
        'na-academy': 'TRLH1',
        'msi': 'TRLH1',
        'rift-rivals': 'ESPORTSTMNT03',
        'worlds': 'TRLH4',
        'all-star': 'WMC2TMNT1',
        'na-scouting-grounds': 'ESPORTSTMNT01'
    }

    def _get_lolsports(self, uri):
        lolsports_url = '{}{}'.format(self.lolsports_rest_api, uri)
        resp = requests.get(lolsports_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()

    def _get_ddragon(self, uri):
        ddragon_url = '{}{}'.format(self.ddragon_rest_api, uri)
        resp = requests.get(ddragon_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()


    def _get_leagueoflegends(self, uri):
        leagueoflegends_url = '{}{}'.format(self.leagueoflegends_rest_api, uri)
        resp = requests.get(leagueoflegends_url)

        if resp.status_code != 200:
            LOG.error("%s: Status code %d", self.ID, resp.status_code)
            LOG.error("%s: Headers: %s", self.ID, resp.headers)
            LOG.error("%s: Resp: %s", self.ID, resp.text)
            resp.raise_for_status()

        return resp.json()


    def items(self):
        return self._get_ddragon('/cdn/8.23.1/data/en_US/item.json')

    def mastery(self):
        return self._get_ddragon('/cdn/7.23.1/data/en_US/mastery.json')

    def champions(self):
        return self._get_ddragon('/cdn/8.23.1/data/en_US/champion.json')

    def champion(self, champion_name):
        return self._get_ddragon('/cdn/8.23.1/data/en_US/champion/{}.json'.format(champion_name))

    def summoner(self):
        return self._get_ddragon('/cdn/8.23.1/data/en_US/summoner.json')

    def leagues(self):
        '''
        get all the possible leagues this api can get data for.
        The response contains the id and slug for each league (which is needed for other api functions)
        '''
        return self._get_lolsports('/v1/navItems')['leagues']


    def league_info(self, league_slug):
        '''
        league_slug: the league you want the info for

        the high level fields from response:
            leagues, highlanderTournaments, highlanderRecords, teams, players
        '''
        return self._get_lolsports('{}{}'.format('/v1/leagues?slug=', league_slug))


    def get_games_in_timeframe(self, league_slug, start_timestamp, end_timestamp):
        '''
        league_slug: league you want the games from
        start_timestamp: epoch time in milliseconds
        end_timestamp: epoch time in milliseconds
        '''
        games = []

        info = self.league_info(league_slug)
        for tournament in info['highlanderTournaments']:
            for bracket_id, bracket in tournament['brackets'].items():
                for match_id, match in bracket['matches'].items():
                    match_time = match['standings']['timestamp']
                    if start_timestamp > match_time and match_time < end_timestamp:
                        for game_id, game in match['games'].items():
                            game['tournament_id'] = tournament['id']
                            game['match_id'] = match_id
                            games.append(game)

        return games


    def scheduled_items(self, league_id):
        '''
        league_id: the league id you want the scheduled items for

        The high level fields from response:
            scheduleItems, highlanderTournaments, teams, highlanderRecords, players

        The scheduleItems field is a list of all scheduled items for a league (the list goes back a long ways)
        '''
        return self._get_lolsports('/v1/scheduleItems?leagueId={}'.format(league_id))


    def scheduled_items_timeframe(self, league_id, start_timestamp, end_timestamp):
        '''
        league_id: the league id you want the scheduled items for
        start_timestamp: epoch time in milliseconds
        end_timestamp: epoch time in milliseconds
        '''
        pattern = '%Y-%m-%d'
        seconds_start = start_timestamp/1000
        seconds_end = end_timestamp/1000

        items_to_return = []

        items = self.scheduled_items(league_id)['scheduleItems']
        for item in items:
            epoch = int(time.mktime(time.strptime(item['scheduledTime'].split('T')[0], pattern)))
            if seconds_start > epoch and epoch < seconds_end:
                items_to_return.append(item)

        return items_to_return


    def match_details(self, tournament_id, match_id):
        '''
        tournament_id: the tournament of the match you want the info for
        match_id: the match you want the info for

        The high level fields from the response:
            teams, players, scheduleItems, gameIdMappings, videos, htmlBlocks
        '''

        return self._get_lolsports(
            '{}{}{}{}'.format(
                '/v2/highlanderMatchDetails?tournamentId=',
                tournament_id,
                '&matchId=',
                match_id
            )
        )


    def game_stats(self, league_slug, game_id, game_hash):
        '''
        to get game_id: league_info['highlanderTournaments'][0]['brackets'][<bracket id>]['matches'][<match id>]['games'][<game id>]['gameId']
        to get game_hash: match_details['gameIdMappings'][0]['gameHash']
        '''

        return self._get_leagueoflegends(
            '{}{}/{}?gameHash={}'.format(
                '/v1/stats/game/',
                self.region_code_mapping[league_slug],
                game_id,
                game_hash
            )
        )

    def game_timeline(self, league_slug, game_id, game_hash):
        '''
        to get game_id: league_info['highlanderTournaments'][0]['brackets'][<bracket id>]['matches'][<match id>]['games'][<game id>]['gameId']
        to get game_hash: match_details['gameIdMappings'][0]['gameHash']

        get frame by frame timeline of the game with all players stats
        '''

        return self._get_leagueoflegends(
            '{}{}/{}/timeline?gameHash={}'.format(
                '/v1/stats/game/',
                self.region_code_mapping[league_slug],
                game_id,
                game_hash
            )
        )