import time

import requests
import pandas as pd

from src.constants import API_KEY, REGION, INFO_KEYS, PARTICIPANT_KEYS, TEAM_KEYS, OBJECTIVES_KEYS, DELAY_API


def call_api(region: str, url: str, params:dict = {}) -> dict | None:
    formatted_url = f"https://{region}.api.riotgames.com{url}?api_key={API_KEY}"
    for key, val in params.items():
        formatted_url += f"&{key}={val}"

    res = requests.get(url=formatted_url)

    if res.status_code == 200:
        return res.json()
    
    raise Exception(f"API error: {res.text}")


def get_player_uuid(region, game_name, tag_line):
    url = f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    return call_api(region, url)['puuid']


def get_last_matches(puuid: str, n_matches: int) -> list[str]:
    url = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {'count': n_matches}
    return call_api(REGION, url, params)


def get_matches_info(matches_ids: list[str]) -> list[dict]:
    matches_info = []
    
    for match_id in matches_ids:
        url = f"/lol/match/v5/matches/{match_id}"
        matches_info.append(call_api(REGION, url))
        time.sleep(DELAY_API)

    return matches_info


def extract_info(puuid: str, matches_info: list[dict]) -> pd.DataFrame:
    filtered_info = []

    for match_info in matches_info:
        player_info = []
        team_id = None

        for key in INFO_KEYS:
            player_info.append(match_info['info'][key])

        for p in match_info['info']['participants']:
            if p['puuid'] == puuid:
                team_id = p['teamId']
                for key in PARTICIPANT_KEYS:
                    player_info.append(p[key])
        
        for t in match_info['info']['teams']:
            if t['teamId'] == team_id:
                for key in TEAM_KEYS:
                    player_info.append(t[key])
                for key in OBJECTIVES_KEYS:
                    player_info.append(t['objectives'][key]['kills'])

        filtered_info.append(player_info)

    df_matches_info = pd.DataFrame(filtered_info, columns=INFO_KEYS+PARTICIPANT_KEYS+TEAM_KEYS+OBJECTIVES_KEYS)

    return df_matches_info


def get_current_game() -> dict:
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"

    res = requests.get(url, verify=False)

    if res.status_code == 200:
        return res.json()
    
    raise Exception(res.text)
