import os
import sys
import glob
import json
from flask_socketio import Namespace
from flask import current_app as app
from .machine import machine
import gevent


def get_job_list():
    job_files = glob.glob(app.config['JOBS_DIR'] + '/*.json')
    job_files.sort()

    jobs = []
    for job_file in job_files:
        jobs.append(job_file.split('/')[-1].replace('.json', ''))
    return jobs


def get_job(name):
    job_file = app.config['JOBS_DIR'] + '/' + name + '.json'
    job_file = 'jobs/' + name + '.json'

    if not os.path.isfile(job_file):
        return None

    with open(job_file) as file:
        data = json.load(file)
        return data


def update_job(name, data):
    job_file = app.config['JOBS_DIR'] + '/' + name + '.json'
    job_file = 'jobs/' + name + '.json'

    if not os.path.isfile(job_file):
        return None

    with open(job_file, "w") as file:
        json.dump(data, file)


def get_feeder_list():
    feeders = json.load(open(app.config['FEEDERS_FILE'], 'r'))

    f = []
    for feeder in feeders:
        f.append({
            'name': feeder['name'],
            'type': feeder['type'],
            'component': feeder['component'],
            'size': feeder['size'],
            'remaining': feeder['remaining'],
            'point': feeder['point']
        })

    return f


def get_feeder(name):
    feeders = json.load(app.config['FEEDERS_FILE'])

    for feeder in feeders:
        if name in feeder['name']:
            return feeder
    return None


def update_feeder(feeder, data):
    feeders = json.load(app.config['FEEDERS_FILE'])

    data = []
    for f in feeders:
        if feeder['name'] in f['name']:
            data.append(feeder)
        else:
            data.append(f)

    with open(app.config['FEEDERS_FILE'], "w") as file:
        json.dump(data, file)


class Status(Namespace):

    def __init__(self, path):
        super().__init__(path)
        self.running_update_task = False

    def on_connect(self):

        def update_status():
            while True:
                status = {"state": "Idle",
                          "position": machine.position}
                self.emit('update', status)
                gevent.sleep(0.1)

        if not self.running_update_task:
            self.running_update_task = True
            gevent.spawn(update_status)


class Position(Namespace):

    def on_get(self):
        try:
            return {'status': 'ok', 'position': machine.position}
        except Exception as e:
            app.logger.error(e)
            return {'status': 'error', 'message': str(e)}

    # def on_update(self, coord):
    #     try:
    #         machine.move('n1', coord)
    #         return {'status': 'ok', 'position': machine.position}
    #     except Exception as e:
    #         app.logger.error(e)
    #         return {'status': 'error', 'message': str(e)}

    def on_home(self):
        try:
            machine.home()
            return {'status': 'ok', 'position': machine.position}
        except Exception as e:
            app.logger.error(e)
            return {'status': 'error', 'message': str(e)}

    def on_jog(self, data):
        try:
            machine.jog(data)
            return {'status': 'ok', 'position': machine.position}
        except Exception as e:
            app.logger.error(e)
            return {'status': 'error', 'message': str(e)}

    def on_park(self, data):
        try:
            machine.park(data['axis'], data['speed_factor'])
            return {'status': 'ok', 'position': machine.position}
        except Exception as e:
            app.logger.exception(str(e))
            return {'status': 'error', 'message': str(e)}


class Actuators(Namespace):

    def on_get(self, name):
        pass

    def on_update(self, name, steps):
        pass

    def on_put(self, name, steps):
        pass


class Job(Namespace):

    def on_get(self, name):
        if "all" in name:
            return get_job_list()
        else:
            return get_job(name)

    def on_update(self, name, steps):
        update_job(name, steps)

    def on_put(self, name, steps):
        pass

    def on_start(self, name):
        job = {'name': name, 'steps': get_job(name)}
        try:
            machine.start_job(job)
            return {'status': 'ok', 'message': 'Job started'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def on_stop(self):
        try:
            machine.stop_job()
            return {'status': 'ok', 'message': 'Job started'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


class Feeders(Namespace):

    def on_get(self, name):
        if "all" in name:
            return get_feeder_list()
        else:
            return get_feeder(name)

    def on_update(self, name, steps):
        pass

    def on_put(self, name, steps):
        pass
