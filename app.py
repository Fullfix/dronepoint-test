from flask import Flask, request
from flask_cors.decorator import cross_origin
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from dotenv import dotenv_values
import time
import logging
from routes.videos import videos as videos_blueprint
from mavlink.Mavlink import Mavlink

# Init App
app = Flask(__name__, static_folder='./client/build', static_url_path='/')
CORS(app, resources={ 'r"*"': { "origins": '*' } })
socketio = SocketIO(app, cors_allowed_origins="*")
config = dotenv_values('.env')
password = config['SECRET_CODE']

# Init mavlink
mavlink = Mavlink()

# Disable logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# Videos blueprint
app.register_blueprint(videos_blueprint, url_prefix='/api/videos')

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

# Get mavlink data
@socketio.on('getdata')
def send_message(json):
    # if json['password'] != password:
    #     return emit('error', 'Invalid password')
    return emit('data', mavlink.get_data())

# Start text
@socketio.on('test')
def start_test(json):
    if not mavlink.check_cell(json['cell']):
        print("Can't start test")
        emit('error', 'Invalid cell')
    if mavlink.connected:
        print(mavlink.connected)
        mavlink.test(json['cell'])
    else:
        print("Can't start test")

if __name__ == "__main__":
    socketio.run(app)