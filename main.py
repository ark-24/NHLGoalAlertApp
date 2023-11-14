from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import psycopg2
from datetime import datetime, timezone, date



def most_recent_team():
    conn = psycopg2.connect(database="nhlgoalalert", user="postgres", 
                        password="password", host="localhost", port="5432") 
    cur = conn.cursor() 
    cur.execute('''SELECT * FROM teams ORDER BY date DESC LIMIT 1''')
    data = cur.fetchone()
    return data[1]

def get_todays_game():
    myurl = 'https://api-web.nhle.com/v1/scoreboard/now'
    today = str(date.today())
    response = requests.get(myurl)
    data = response.json()
    gamesByDate = data['gamesByDate']
    for gameDay in gamesByDate:
        if gameDay['date'] == today:
            return gameDay['games']


if __name__ == "__main__":
    team = most_recent_team()
    print(team)
    gamesToday = get_todays_game()
    # for games in gamesToday:


