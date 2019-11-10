import os
from flask_migrate import Migrate
from config import init_app_config, init_logging
from app import app as flask_app, db


def setup(app, **kwargs):
    from api.models import user, cluster, machine, identifier
    init_logging(**kwargs)
    init_app_config(app, **kwargs)
    db.init_app(app)
    return app


application = setup(flask_app, **os.environ)
migrate = Migrate(application, db)
