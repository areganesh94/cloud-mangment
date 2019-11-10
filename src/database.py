from flask_sqlalchemy import SQLAlchemy as BaseSQL

class SQLAlchemy(BaseSQL):
    def apply_pool_defaults(self, app, options):
        options.setdefault('pool_pre_ping', app.config['SQLALCHEMY_POOL_PRE_PING'])
        super(SQLAlchemy, self).apply_pool_defaults(app, options)