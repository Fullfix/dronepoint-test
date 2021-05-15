from flask import Flask
from flask_socketio import SocketIO, emit, send
import time
import logging
from mavlink.Mavlink import Mavlink

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
mavlink = Mavlink()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return { "text": 'Hello World' }

@socketio.on('getdata')
def send_message():
    return emit('data', mavlink.get_data())

@socketio.on('test')
def start_test():
    if mavlink.connected:
        print(mavlink.connected, mavlink.connected())
        # mavlink.test()
    else:
        print("Can't start test")

if __name__ == "__main__":
    socketio.run(app)