import logging, sys
from flask_log_request_id import RequestIDLogFilter

logger = logging.getLogger(__name__)


def init_logging(**kwargs):
    logging.basicConfig(
        level=kwargs.get('LOG_LEVEL', 'INFO'),
        stream=sys.stderr)
    for handler in logging.getLogger().handlers:
    	handler.addFilter(RequestIDLogFilter())
    	handler.setFormatter(logging.Formatter(
    		"%(asctime)s:%(request_id)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d:%(message)s"))

def init_app_config(app, **kwargs):
	app.config['VERSION'] = kwargs.get('VERSION', '0.0.0')
	init_logging(**kwargs)
	app.config['APPS'] = ['apis']
	app.config['SQLALCHEMY_DATABASE_URI'] = kwargs['DATABASE_URL']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	logger.info('Basic Requirments Set')