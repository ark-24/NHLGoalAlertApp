from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from datetime import datetime


app = Flask(__name__)
CORS(app)



@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': 'hello world'
    })
@app.route("/api/saveTeams", methods=['POST'])
def save_teams():
    conn = psycopg2.connect(database="nhlgoalalert", user="postgres", 
                        password="password", host="localhost", port="5432") 
  
# create a cursor 
    cur = conn.cursor() 
    teamName = request.form['name']
    id = request.form['id']
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
