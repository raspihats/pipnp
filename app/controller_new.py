from flask import current_app as app
import os
import glob
import json


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


def register_events(socketio, logger):

    @socketio.on('connect')
    def on_connect():
        logger.info('Connected')

    @socketio.on('get_job_list')
    def on_get_job_list():
        socketio.emit('job_list', get_job_list())

    @socketio.on('get_job_details')
    def on_get_job_details(name):
        socketio.emit('job_details', get_job(name))
