from flask_restplus import Api, Resource, Namespace, fields
from ..service.position_service import get_position, set_position

api = Namespace('position', description='Machine position')

position = api.model('Position', {
    "x": fields.Float(readOnly=True, description='x coordinate'),
    "y": fields.Float(readOnly=True, description='y coordinate'),
})


@api.route('/')
class Position(Resource):
    current_position = {
        'x': 5,
        'y': 5
    }

    '''Show a single job item and lets you delete them'''
    @api.doc('get_position')
    @api.marshal_with(position)
    def get(self):
        '''Get the current position'''
        # api.abort(500, "Job {} doesn't exist".format(name))
        return get_position()

    @api.expect(position)
    @api.marshal_with(position)
    def put(self):
        '''Move to position'''
        set_position(api.payload)
