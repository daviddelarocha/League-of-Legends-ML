import time

from src.constants import REGION, GAME_NAME, TAG_LINE
from src import api, model

PUUID = api.get_player_uuid(REGION, GAME_NAME, TAG_LINE)
MODEL = model.load_model(PUUID)


def main():
    print("Welcome")
    while True:
        print("Getting info...")
        ## get info
        df_info = api.extract_info(
            PUUID,
            api.get_matches_info(api.get_last_matches(PUUID, 1)) 
        )
        ## clean data
        X = model.clean_data(df_info)
        Y = X['win'].values
        X = X.drop(columns=['win'])

        print("Doing prediction...")
        ## predict
        prob_pred = model.predict(MODEL, X)

        ## visualize
        print("\nWinning probability: ", prob_pred)
        print("\nVictory: ", Y)
        print("\nStats: \n", X.T)

        ## delay
        time.sleep(5)


if __name__ == "__main__":
    main()