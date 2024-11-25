import os

import pandas as pd

from src.constants import REGION, GAME_NAME, TAG_LINE
from src import api, model

PUUID = api.get_player_uuid(REGION, GAME_NAME, TAG_LINE)


def main():
    ## get info
    print("Getting info...")
    filename = f"data/data_{PUUID}.csv"
    if os.path.isfile(filename):
        df_info = pd.read_csv(filename)
    else:
        df_info = api.extract_info(
            PUUID,
            api.get_matches_info(api.get_last_matches(PUUID, 100)) 
        )
        df_info.to_csv(filename)

    ## clean data
    print("Cleaning data...")
    data = model.clean_data(df_info)

    ## train model
    print("Training model...")
    t_model = model.train_model(data)

    ## save model
    print("Saving model...")
    model.save_model(t_model, PUUID)

if __name__ == "__main__":
    main()