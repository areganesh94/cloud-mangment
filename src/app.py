import pdb, logging

from config import init_app_config
from flask import Flask
from flask_log_request_id import RequestID
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

app = Flask(__name__)
db = SQLAlchemy()

def setup(app, **kwargs):
	RequestID(app)
	init_app_config(app, **kwargs)
	# pdb.set_trace()

	return app



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
    app.url_map.strict_slashes = False
    application = setup(app, **os.environ)
    application.run(host=args.host, port=args.port, debug=args.debug)
