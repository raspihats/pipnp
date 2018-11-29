# Import flask and template operators
import logging
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from .machine import machine
from .controller_new import register_events

app = Flask(__name__)
app.config.from_object('config')

Bootstrap(app)
socketio = SocketIO(app)


class SocketIOHandler(logging.StreamHandler):
    def emit(self, message):
        socketio.emit('log', self.format(message))


logger = logging.getLogger('fe_logger')
logger.handlers = []

ch = SocketIOHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

register_events(socketio, logger)


@app.route('/')
def index():
    return render_template('index.html')


# @socketio.on('connect')
# def on_connect():
#     logger.info('Connected')


def run_app():
    try:
        machine.logger = logger
        # machine.open()
        # machine.home()
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        print("Finally_app_id: ", '{}'.format(id(app)))
        machine.close()
