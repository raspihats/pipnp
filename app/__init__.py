# Import flask and template operators
import logging
from flask import Flask, Response, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from .machine import machine
# from .controller_new import register_events
from .controller import Position, Job
from gevent import sleep
import cv2

app = Flask(__name__)
app.config.from_object('config')

Bootstrap(app)
socketio = SocketIO(app, async_mode='gevent')


class SocketIOHandler(logging.StreamHandler):
    def emit(self, message):
        socketio.emit('log', self.format(message))


# logger = logging.getLogger('fe_logger')
# logger.handlers = []

ch = SocketIOHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
app.logger.addHandler(ch)
app.logger.setLevel(logging.DEBUG)

# register_events(socketio, logger)

socketio.on_namespace(Position('/position'))
socketio.on_namespace(Job('/job'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_frame():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)  # this makes a web cam object
    while True:
        ret, frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        sleep(0.02)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    del(camera)


# @socketio.on('connect')
# def on_connect():
#     logger.info('Connected')


def run_app():
    try:
        machine.logger = app.logger
        machine.open()
        machine.home()
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        print("Finally_app_id: ", '{}'.format(id(app)))
        machine.close()
