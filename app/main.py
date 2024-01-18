import sys
import pickle
import uvicorn
import pandas as pd
from fastapi import FastAPI

#Start API
app = FastAPI()

#Load model
sys.path.append('src')
with open('models/recommender.pkl', 'rb') as file:
    recommender = pickle.load(file)

#Create home page
@app.get('/')
def home():
    return 'Welcome to the Steam game Recommender app!'

#List games
@app.get('/list_games')
def list_games():
    return recommender.scores_.index.tolist()

#Search games from substring
@app.get('/search_games')
def search_games(pattern):
    pattern = pattern.lower()
    games = pd.Series(recommender.scores_.index.tolist())
    games_matched = games[games.str.lower().str.contains(pattern)]
    return games_matched

#Recommend games
@app.get('/recommend')
def recommend(game: str, max_recommendations: int = 10):
    return recommender.recommend(game, max_recommendations)

#Execute API
if __name__ == '__main__':
    uvicorn.run(app)