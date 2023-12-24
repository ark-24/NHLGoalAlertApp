import requests
import psycopg2
from datetime import date
import boto3
import pygame

s3 = boto3.client('s3')
BUCKET_NAME = "nhlgoalhorns"


def most_recent_team():
    conn = psycopg2.connect(database="nhlgoalalert", user="postgres", 
                        password="password", host="localhost", port="5432") 
    cur = conn.cursor() 
    cur.execute('''SELECT * FROM teams ORDER BY date DESC LIMIT 1''')
    data = cur.fetchone()
    return data[1]

def get_current_game():
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
    currGame = get_current_game()
    if currGame["awayTeam"]["name"]["default"] == team:
        return "awayTeam"
    else:
         return "homeTeam"

def create_folders():
    #create team folders to store goal horns in aws s3
    teams = []
    url = "https://api-web.nhle.com/v1/standings/now"
    response = requests.get(url)
    data = response.json()
    for elem in data['standings']:
        teams.append(elem['teamName']['default'])
    teams.sort()
    for team in teams:
        s3.put_object(Bucket=BUCKET_NAME, Key=(team+'/'))

def get_goal_horn(team):
    #retrieve goal horns from s3 and play
    path = team+'/'+team.lower()+'.wav'
    response = s3.get_object(Bucket=BUCKET_NAME, Key=path)
    audio_data = response['Body'].read()

    with open("goalhorn.wav", "wb") as fp:
        fp.write(audio_data)
    fp.close()

def play_goal_song():
    pygame.mixer.init()
    pygame.mixer.music.load("goalhorn.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

if __name__ == "__main__":
    team = most_recent_team()
    gamesToday = get_current_game()
    currGame = get_current_game()
    get_goal_horn(team)

    if currGame:
        whichSide = isHomeOrAwayTeam(team)
        score = currGame[whichSide]["score"]

        while currGame["gameState"] == "LIVE" or currGame["gameState"] == "CRIT":
            currGame = get_current_game()
            currScore = currGame[whichSide]["score"]
            if currScore > score:
                score = currScore
                play_goal_song()


    
            


