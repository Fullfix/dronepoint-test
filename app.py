from flask import Flask, request
from flask_cors.decorator import cross_origin
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from dotenv import dotenv_values
import time
import logging
from mavlink.Mavlink import Mavlink

# Init App
app = Flask(__name__)
CORS(app, resources={ 'r"*"': { "origins": '*' } })
socketio = SocketIO(app, cors_allowed_origins="*")
config = dotenv_values('.env')
password = config['SECRET_CODE']

# Init mavlink
mavlink = Mavlink()

# # Disable logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# Compare passwords
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    if data['password'] == password:
        return { "text": 'Authenticated' }
    return { "text": "Wrong password" }, 400

# Get mavlink data
@socketio.on('getdata')
def send_message(json):
    if json['password'] != password:
        return emit('error', 'Invalid password')
    return emit('data', mavlink.get_data())

# Start text
@socketio.on('test')
def start_test(json):
    if json['password'] != password:
        return emit('error', 'Invalid password')
    if mavlink.connected:
        print(mavlink.connected, mavlink.connected())
        # mavlink.test()
    else:
        print("Can't start test")

if __name__ == "__main__":
    socketio.run(app)