from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/home", methods=['GET'])
def return_home():
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
