from flask_cors import CORS, cross_origin
from flask import Flask
from flask_restful import Api
from resources.questionnaire import Questionnaire
from resources.question import UpdateQuestion
from resources.message import UpdateMessage

app = Flask(__name__)

api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


api.add_resource(Questionnaire, "/api/questionnaire")
api.add_resource(UpdateMessage, "/api/message/update")
api.add_resource(UpdateQuestion, "/api/question/update")

if __name__ == "__main__":
    app.run()
