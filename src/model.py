import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score

from src.constants import ROLES


def clean_data(df_info: pd.DataFrame) -> pd.DataFrame:
    data = df_info.copy()

    ## filter game mode
    data = data[data['gameMode'] == 'CLASSIC']
    data = data.drop(columns=["gameMode"])

    ## replace teamPosition to numerical
    data['teamPosition'] = data['teamPosition'].replace(ROLES)

    ## set column 'win' to numerical
    data['win'] = data['win'].astype(int)

    ## drop empty values
    data = data.dropna()

    return data


def train_model(data):
    X = data.drop(columns=['win'])
    Y = data['win']

    ## Decompose training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.15)
    
    ## Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    ## Evaluate
    evaluate_model(model, X_test, y_test)


def evaluate_model(model, X_test, y_test):
    ## Make a prediction
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] # positive class

    ## Evaluate
    print("Accurary:", accuracy_score(y_test, y_pred))
    print("ROC-AUC", roc_auc_score(y_test, y_pred_proba))
    print("\nClassification report\n", classification_report(y_test, y_pred))


def load_model(puuid, model_type="random_forest"):
    loaded_model = joblib.load(f'data/{model_type}_{puuid}.pkl')
    return loaded_model


def predict(model, X, proba=False):
    if proba:
        return model.predict(X)
    
    return model.predict_proba(X)[:, 1]