# Import flask and template operators
import logging
from flask import Flask, Blueprint, render_template
from flask_restplus import Api, apidoc
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from .controller.job_controller import api as job_ns
from .controller.position_controller import api as position_ns
from .machine import machine

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)


@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)


app.register_blueprint(blueprint)

api.add_namespace(job_ns)
api.add_namespace(position_ns)

Bootstrap(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


class SioHandler(logging.StreamHandler):
    def emit(self, message):
        print(self.format(message))
        socketio.emit('log', self.format(message))


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

logger = logging.getLogger('simple_example')
ch = SioHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@socketio.on('connect')
def test_connect():
    socketio.emit('log', 'Connected')


def run_app():
    try:
        machine.logger = logger
        machine.open()
        machine.home()
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        print("Finally_app_id: ", '{}'.format(id(app)))
        machine.close()
