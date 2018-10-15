"""
Main app root of the api endpoints
"""
from flasgger import Swagger
from flask import Flask, redirect
from flask_cors import CORS

from api.config.config import DevelopmentConfig, HostConfig
from api.models.database import DatabaseConnection
from api.routes import Urls


class Server:
    """
    Creates the flask object to start the server
    """

    @staticmethod
    def create_app(env=None):
        app = Flask(__name__)
        Swagger(app)
        app.config.update(env.__dict__ or {})
        Urls.generate(app)
        CORS(app)
        with app.app_context():
            database = DatabaseConnection()
            database.init_db(app)
        return app


APP = Server().create_app(env=DevelopmentConfig)


@APP.route("/")
def main():
    return redirect('/apidocs')


if __name__ == '__main__':
    APP.run(host=HostConfig.HOST, port=HostConfig.PORT)