from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.question import QuestionModel
from flask import Flask
from flask import request

class UpdateQuestion(Resource):
    parser = reqparse.RequestParser()
    def post(self):
        self.parser.add_argument('rating', location='json')
        self.parser.add_argument('qId', type=str, help='Question Id is mandatory', required=True)
        self.parser.add_argument('qa', type=str, help='Question is mandatory', required=True)
        args = self.parser.parse_args()
        content = request.get_json()
        result = QuestionModel.updateQuestion(args, content)
        if result:
            return {"result": result, "error": "null", "statusCode": 200}, 200
        return { "result": [], "error": "", "statusCode": 200}, 200
