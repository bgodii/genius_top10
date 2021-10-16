from flask import Flask
from flask_restful import Api

from views.top_songs import TopSongs

APP = Flask(__name__)
API = Api(APP)

API.add_resource(TopSongs, "/top10")

APP.run(host="0.0.0.0", port=8080, debug=True)
