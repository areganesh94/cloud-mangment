import logging

from config import init_app_config
from flask import Flask
from flask_log_request_id import RequestID
from database import SQLAlchemy
from blueprint import RegisterBlueprint

logger = logging.getLogger(__name__)

app = Flask(__name__)
db = SQLAlchemy()


def setup(app, **kwargs):
    global db
    db.init_app(app)
    RequestID(app)
    init_app_config(app, **kwargs)
    registered_blueprint = RegisterBlueprint(app.config['APPS'])
    for blueprint in registered_blueprint.blueprint:
        app.register_blueprint(blueprint)
    return app


@app.route('/healthcheck')
def healthcheck():
    return "OK"


@app.route('/version')
def version():
    return app.config.get('VERSION', '0.0.0')


if __name__ == "__main__":
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str,
                        default="0.0.0.0", help="Host IP address to bind to")
    parser.add_argument('-P', '--port', type=int,
                        default=5000, help="Host port to listen on")
    parser.add_argument('-D', '--debug', type=bool,
                        default=True, help="Debug mode")
    args = parser.parse_args()
    application = setup(app, **os.environ)
    application.url_map.strict_slashes = False
    if application.debug:
        print(app.url_map)
    application.run(host=args.host, port=args.port, debug=args.debug)
