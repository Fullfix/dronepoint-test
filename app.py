from flask import Flask, request
from flask_cors.decorator import cross_origin
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from dotenv import dotenv_values
import time
import logging
from routes.videos import dp_camera, drone_camera
from mavlink.Mavlink import Mavlink
from config import password

# Init App
app = Flask(__name__, static_folder='./client/build', static_url_path='/')
CORS(app, resources={ 'r"*"': { "origins": '*' } })
socketio = SocketIO(app, cors_allowed_origins="*")

# Init mavlink
mavlink = Mavlink()

# Disable logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Videos blueprint
# app.register_blueprint(videos_blueprint, url_prefix='/api/videos')

# React app
@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')

# Compare passwords
@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    # if data['password'] == password:
    #     return { "text": 'Authenticated' }
    # return { "text": "Wrong password" }, 400
    return { 'text': 'Done' }

# Send video
@socketio.on('getvideo')
def send_video():
    return emit('video', {
        'dronepoint': dp_camera.lastframe,
        'drone': drone_camera.lastframe,
    })

# Get mavlink data
@socketio.on('getdata')
def send_message(json):
    # if json['password'] != password:
    #     return emit('error', 'Invalid password')
    return emit('data', mavlink.get_data())

# Start text
@socketio.on('test')
def start_test(json):
    if json['password'] != password:
        return emit('error', 'Invalid Password')
    if not mavlink.check_cell(json['cell']):
        print("Can't start test")
        return emit('error', 'Invalid cell')
    if mavlink.connected:
        print(mavlink.connected)
        mavlink.test(json['cell'])
    else:
        emit('error', "Can't start dronepoint test")
        print("Can't start test")


if __name__ == "__main__":
    socketio.run(app)