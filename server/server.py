
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import psycopg2
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

@app.route("/api/nhl-proxy", methods=['GET'])
def nhl_proxy():
    try:
        # Make the request to the NHL API
        myurl = "https://api.nhle.com/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id"
        response = requests.get(myurl)
        data = response.json()
        return jsonify(data['data'])
    except Exception as e:
        print(f"Error fetching data from NHL API: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': 'hello world'
    })


@app.route("/api/saveTeams", methods=['POST'])
def save_teams():
    conn = psycopg2.connect(database="nhlgoalalert", user="postgres", 
                        password="password", host="localhost", port="5432") 
    dt_string = datetime.now(timezone.utc)
    
  
# create a cursor 
    cur = conn.cursor() 
    data = request.get_json()
    print(data)
    teamName = data.get('label')
    id = data.get('value')

    cur.execute( '''INSERT INTO teams  
        (id, teamnames, date) VALUES (%s, %s, %s)''', 
        (id, teamName,dt_string )) 
# commit the changes 
    conn.commit() 
  
# close the cursor and connection 
    cur.close() 
    conn.close() 
    return jsonify({
        'message': 'hello world'
    })

@app.route("/", methods=['GET'])
def landing():
    return jsonify({
        'message': 'hello world'
    })


if __name__ == "__main__":
    app.run(debug=True,port=8080) #remove arg if deploying to prod
