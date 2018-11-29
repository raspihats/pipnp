from flask import current_app as app
import os
import json
import glob


# def save_new_user(data):
#     user = User.query.filter_by(email=data['email']).first()
#     if not user:
#         new_user = User(
#             public_id=str(uuid.uuid4()),
#             email=data['email'],
#             username=data['username'],
#             password=data['password'],
#             registered_on=datetime.datetime.utcnow()
#         )
#         save_changes(new_user)
#         response_object = {
#             'status': 'success',
#             'message': 'Successfully registered.'
#         }
#         return response_object, 201
#     else:
#         response_object = {
#             'status': 'fail',
#             'message': 'User already exists. Please Log in.',
#         }
#         return response_object, 409


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


# def save_changes(data):
#     db.session.add(data)
#     db.session.commit()
