from flask.blueprints import Blueprint
from flask import Response
import cv2

# Init camera
camera = cv2.VideoCapture('rtsp://192.168.194.111:8554/video')

# Get frame from camera
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

videos = Blueprint('videos', __name__)

# Dronepoint camera
@videos.route('/dronepoint')
def stream_dronepoint():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')