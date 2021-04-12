from flask import Flask
from flask_socketio import SocketIO, emit, send
import time
from mavlink.Mavlink import Mavlink

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
mavlink = Mavlink()

@app.route('/')
def index():
    return { "text": 'Hello World' }

@socketio.on('getdata')
def send_message():
    return emit('data', mavlink.get_data())

@socketio.on('test')
def start_test():
    mavlink.test()

if __name__ == "__main__":
    socketio.run(app)