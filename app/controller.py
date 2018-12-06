import os
import glob
import json
from flask_socketio import Namespace
from flask import current_app as app
from .machine import machine


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
            machine.park(data)
            return {'status': 'ok', 'position': machine.position}
        except Exception as e:
            app.logger.error(e)
            return {'status': 'error', 'message': str(e)}
