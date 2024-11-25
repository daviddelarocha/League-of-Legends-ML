import time
import matplotlib.pyplot as plt
import streamlit as st
from src.constants import REGION, GAME_NAME, TAG_LINE
from src import api, model

# Load the model
PUUID = api.get_player_uuid(REGION, GAME_NAME, TAG_LINE)
MODEL = model.load_model(PUUID)

# List to store win probability history
win_probability_history = {}

def main():
    # Page configuration
    st.set_page_config(page_title="League of Legends Predictor", page_icon=":guardsman:", layout="centered")
    
    st.title(f"LoL Match Win Prediction")
    
    # Display static player information
    st.subheader(f"{GAME_NAME} ({REGION})")
    
    # Persistent placeholders
    game_duration_placeholder = st.empty()
    prob_placeholder = st.empty()
    col5, col6, col7 = st.columns([1, 1, 1.5])  # For player stats, team stats, and graph
    player_stats_placeholder = col5.empty()
    team_stats_placeholder = col6.empty()
    graph_placeholder = col7.empty()
    
    while True:
        # Retrieve information
        df_info = api.extract_info(
            PUUID,
            api.get_matches_info(api.get_last_matches(PUUID, 1)) 
        )
        
        # Clean data
        X = model.clean_data(df_info)
        Y = X['win'].values
        X = X.drop(columns=['win'])

        # Make prediction
        prob_pred = model.predict(MODEL, X)

        # Update win probability history
        duration = df_info['gameDuration'].values[0] / 60
        win_probability_history[duration] = prob_pred[0]

        # arrange_data
        X = X.drop(columns=['gameDuration', 'assists', 'championId', 'deaths', 'kills', 'teamPosition'])
        player_stats = X.iloc[:, :8].rename({0: 'value'})
        player_stats['kda'] = "/".join(map(str, df_info[['kills', 'deaths', 'assists']].values[0]))
        cols = ['kda'] + list(player_stats.columns[:-1])
        player_stats = player_stats[cols]
        team_stats = X.iloc[:, 8:].rename({0: 'value'})

        # Update Game Duration
        game_duration_placeholder.subheader(f"Game Duration: {int(duration)} minutes")
        
        # Update Win Probability with color coding
        prob_color = "green" if prob_pred[0] > 0.6 else "red"
        prob_placeholder.markdown(f"""
        <div style="background-color:#f0f8ff; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
            <span style="font-size:24px; font-weight:bold; color:{prob_color};">Win Probability: {prob_pred[0]:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        # Update Player Statistics
        player_stats_placeholder.write("**Player Statistics:**")
        player_stats_placeholder.dataframe(player_stats.T)

        # Update Team Statistics
        team_stats_placeholder.write("**Team Statistics:**")
        team_stats_placeholder.dataframe(team_stats.T)

        # Update Graph
        fig, ax = plt.subplots()
        ax.plot(win_probability_history.keys(), win_probability_history.values(), color="blue", marker="o")
        ax.set_title("Win Probability Over Time")
        ax.set_xlabel("Game Duration (minutes)")
        ax.set_ylabel("Win Probability")
        ax.axhline(y=0.6, color="green", linestyle="--", label="High Win Probability Threshold")
        ax.legend()
        graph_placeholder.pyplot(fig)

        # Delay
        time.sleep(5)

if __name__ == "__main__":
    main()
