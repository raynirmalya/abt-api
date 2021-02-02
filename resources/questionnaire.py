from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.questionnaire import QuestionnaireModel

class Questionnaire(Resource):
    parser = reqparse.RequestParser()
    def get(self):
        questions = QuestionnaireModel().getAllQuestions()
        if questions:
            return {"result": questions, "error": "null", "statusCode": 200}, 200
        return { "result": [], "error": questions, "statusCode": 200}, 200
