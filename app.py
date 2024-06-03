from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to fetch COVID-19 data
@app.route('/api/data')
def get_data():
    response = requests.get('https://api.covid19india.org/data.json')
    data = response.json()
    return jsonify(data)

# WebSocket route for real-time updates
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_data')
def handle_request_data():
    response = requests.get('https://api.covid19india.org/data.json')
    data = response.json()
    emit('update_data', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)

