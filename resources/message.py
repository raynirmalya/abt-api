from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.message import MessageModel

class UpdateMessage(Resource):
    parser = reqparse.RequestParser()
    def post(self):
        self.parser.add_argument('message', type=str, help='Message is mandatory', required=True)
        self.parser.add_argument('subMessage', type=str, help='Sub Message is mandatory', required=True)
        self.parser.add_argument('qId', type=str, help='Question Id is mandatory', required=True)
        args = self.parser.parse_args()
        result = MessageModel.updateMessage(args)
        if result:
            return {"result": result, "error": "null", "statusCode": 200}, 200
        return { "result": [], "error": "", "statusCode": 200}, 200
