import pandas as pd

from src.constants import GAME_NAME, TAG_LINE, FINAL_COLUMNS, CHAMPS_IDS, ROLES
from src.api import get_current_game


FUNCTIONAL_CASE = False
CURRENT_PLAYER: dict = None
TEAM: str = None
TEAM_MATES = set([])
EVENTS_COUNT = 0
BARON = 0
CHAMPION = 0
DRAGON = 0
INHIBITOR = 0
RIFTHERALD = 0
TOWER = 0


def fetch_data() -> pd.DataFrame:
    global FUNCTIONAL_CASE, CURRENT_PLAYER, TEAM, TEAM_MATES
    global EVENTS_COUNT, BARON, CHAMPION, DRAGON, INHIBITOR, RIFTHERALD, TOWER

    ## request data
    try:
        raw_data = get_current_game()
    except Exception:
        return None

    ## subdivide by categories
    game_data: dict = raw_data["gameData"]
    active_player: dict = raw_data["activePlayer"]
    events: dict = raw_data["events"]["Events"]

    ## non-functionnal case
    if not FUNCTIONAL_CASE:
        if (game_data["gameMode"] != "CLASSIC" or 
            active_player["riotIdGameName"] != GAME_NAME or
            active_player["riotIdTagLine"] != TAG_LINE):
            return None
        FUNCTIONAL_CASE = True
    
    ## get current player info
    if not CURRENT_PLAYER:
        for player in raw_data["allPlayers"]:
            if player["riotIdGameName"] == GAME_NAME:
                current_player = player
                TEAM = player["team"]
                break

    ## get teammates
    if not TEAM_MATES:
        for player in raw_data["allPlayers"]:
            if player["team"] == TEAM:
                TEAM_MATES.add(player["summonerName"])

    ## add events
    for event in events[EVENTS_COUNT:]:
        if event["EventName"] == "ChampionKill":
            if event["KillerName"] in TEAM_MATES:
                CHAMPION += 1
        elif event["EventName"] == "TurretKilled":
            TOWER += 1
        elif event["EventName"] == "DragonKill":
            DRAGON += 1
        elif event["EventName"] == "HeraldKill":
            RIFTHERALD += 1
        elif event["EventName"] == "InhibKilled":
            INHIBITOR += 1

        EVENTS_COUNT += 1

    ## arrange data
    data = [[
        game_data["gameTime"],
        current_player["scores"]["assists"],
        current_player["level"],
        CHAMPS_IDS[current_player["championName"]],
        current_player["scores"]["deaths"],
        active_player["currentGold"],
        current_player["scores"]["kills"],
        ROLES[current_player["position"]],
        current_player["scores"]["creepScore"],
        current_player["scores"]["wardScore"],
        BARON,
        CHAMPION,
        DRAGON,
        INHIBITOR,
        RIFTHERALD,
        TOWER
    ]]

    return pd.DataFrame(data, columns=FINAL_COLUMNS[:-1])
