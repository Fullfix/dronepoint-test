from flask.blueprints import Blueprint
from flask import Response
import time
import cv2
import threading
from config import stream_video

class DPCamera:
    def __init__(self, url):
        self.lastframe = None
        if stream_video:
            self.camera = cv2.VideoCapture(url)
            gen_thread = threading.Thread(target=self.generate_frames)
            gen_thread.start()
            print('started DP Camera stream')
    
    def generate_frames(self):
        while True:
            success, frame = self.camera.read()
            if success:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # concat frame one by one and show result
                # frame = (b'--frame\r\n'
                #     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                self.lastframe = frame

# Init camera
dp_camera = DPCamera('rtsp://192.168.194.121:8554/video')
drone_camera = DPCamera('http://192.168.194.120:8080/stream?topic=/main_camera/image_raw')

# # Dronepoint camera
# @videos.route('/dronepoint')
# def stream_dronepoint():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')