import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/"
HEADERS = {"x-apisports-key": API_KEY}

def get_fixtures(league_id, season):
    url = f"{BASE_URL}fixtures?league={league_id}&season={season}"
    resp = requests.get(url, headers=HEADERS)
    return resp.json().get("response", [])

def get_team_form(team_id):
    url = f"{BASE_URL}teams/statistics?team={team_id}"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json().get("response", {})
    form_str = data.get("form", "WWDWD")
    return [1 if x=="W" else 0.5 if x=="D" else 0 for x in form_str[:5]]

def get_h2h(home_id, away_id):
    url = f"{BASE_URL}fixtures/headtohead?h2h={home_id}-{away_id}"
    resp = requests.get(url, headers=HEADERS)
    h2h = resp.json().get("response", [])
    home_wins = sum(1 for m in h2h if m['teams']['home']['winner'])
    total = len(h2h) if len(h2h)>0 else 1
    return home_wins / total

def get_players_statistics(team_id):
    url = f"{BASE_URL}players?team={team_id}&season=2025"
    resp = requests.get(url, headers=HEADERS)
    players = resp.json().get("response", [])
    player_scores = {}
    for p in players:
        stats = p.get("statistics", [])
        if stats:
            last_5 = stats[0].get('games', {}).get('appearances', [])[:5]
            score = sum([1 if m else 0 for m in last_5])
            player_scores[p['player']['name']] = score
    return player_scores

def get_injuries(team_id):
    url = f"{BASE_URL}players/injuries?team={team_id}"
    resp = requests.get(url, headers=HEADERS)
    players = resp.json().get("response", [])
    return [p['player']['name'] for p in players if p['injury']]
