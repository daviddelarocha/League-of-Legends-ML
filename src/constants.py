import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
REGION = os.getenv("REGION")
SUB_REGION = os.getenv("SUB_REGION")
GAME_NAME = os.getenv("GAME_NAME")
TAG_LINE = os.getenv("TAG_LINE")

INFO_KEYS = [
    'gameDuration',
    'gameMode'
]

PARTICIPANT_KEYS = [
    'assists',
    'champExperience',
    'champLevel',
    'championId',
    'deaths',
    'goldEarned',
    'kills',
    'neutralMinionsKilled',
    'teamPosition',
    'totalDamageDealt',
    'totalDamageTaken',
    'totalMinionsKilled',
    'visionScore'
]

TEAM_KEYS = [
    'win'
]

OBJECTIVES_KEYS = [
    'baron',
    'champion',
    'dragon',
    'horde',
    'inhibitor',
    'riftHerald',
    'tower'
]

ROLES = {
    "BOTTOM": 1,
    "UTILITY": 2,
    "MIDDLE": 3,
    "JUNGLE": 4,
    "TOP": 5
}
