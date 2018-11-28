from flask_restplus import Api, Resource, Namespace, fields
from ..service.job_service import get_job_list, get_job

api = Namespace('job', description='Machine job')

component = api.model('Component', {
    "name": fields.String(readOnly=True, description='component name'),
    "value": fields.String(readOnly=True, description='component value'),
    "package": fields.String(readOnly=True, description='component package'),
    "x": fields.Float(readOnly=True, description='component x coordinate'),
    "y": fields.Float(readOnly=True, description='component y coordinate'),
    "angle": fields.Float(readOnly=True, description='component rotation angle'),
    "type": fields.String(readOnly=True, description='component type')
})

# job = fields.List(fields.Nested(component))


@api.route('/')
class JobList(Resource):
    '''Shows a list of all jobs, and lets you POST to add new jobs'''
    @api.doc('list_jobs')
    # @api.marshal_list_with(job)
    def get(self):
        '''List all jobs'''
        return get_job_list()

    # @api.doc('create_job')
    # @api.expect(job)
    # @api.marshal_with(job, code=201)
    # def post(self):
    #     '''Create a new job'''
    #     with open(api.payload['name'], 'x') as outfile:
    #         for line in api.payload['lines']:
    #             outfile.write(line + '\n')
    #     return DAO.create(api.payload), 201


@api.route('/<string:name>')
@api.response(404, 'Job not found')
@api.param('name', 'The job name')
class Job(Resource):
    '''Show a single job item and lets you delete them'''
    @api.doc('get_job')
    # @api.marshal_with(job)
    @api.marshal_list_with(component)
    def get(self, name):
        '''Get a specific job'''
        job = get_job(name)
        if job is None:
            api.abort(404, "Job {} doesn't exist".format(name))
        return job

#     @api.doc('delete_todo')
#     @api.response(204, 'Todo deleted')
#     def delete(self, id):
#         '''Delete a task given its identifier'''
#         DAO.delete(id)
#         return '', 204

#     @api.expect(todo)
#     @api.marshal_with(todo)
#     def put(self, id):
#         '''Update a task given its identifier'''
#         return DAO.update(id, api.payload)
