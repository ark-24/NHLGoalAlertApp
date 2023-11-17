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
            for game in gameDay['games']:
                if game["awayTeam"]["name"]["default"] == team or game["homeTeam"]["name"]["default"] == team:
                    return game
    

def isHomeOrAwayTeam(team):
    currGame = get_todays_game()
    if currGame["awayTeam"]["name"]["default"] == team:
        print("in if")
        return "awayTeam"
    else:
        print("in else")

        return "homeTeam"
    
if __name__ == "__main__":
    team = most_recent_team()
    gamesToday = get_todays_game()
    currGame = get_todays_game()
    if currGame:
        whichSide = isHomeOrAwayTeam(team)
        score = currGame[whichSide]["score"]

        print(currGame["gameState"])
        while currGame["gameState"] == "LIVE" or currGame["gameState"] == "CRIT":
            currGame = get_todays_game()
            currScore = currGame[whichSide]["score"]
            if currScore > score:
                print("GOAL!!!!!!!!!!!!!!!!!!!")
                score = currScore


    
            


