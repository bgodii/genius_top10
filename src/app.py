from flask import Flask
from flask_restful import Api, Resource

APP = Flask(__name__)
API = Api(APP)


class HelloWorld(Resource):
    def get(self):
        return {"message": "olá mundo"}, 200


API.add_resource(HelloWorld, "/")

APP.run(host="0.0.0.0", port=8080, debug=False)
