import uuid
import logging
from app import db

logger = logging.getLogger(__name__)

instance_type = {
    'micro': 1,
    'large': 2,
}

class user(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    user_external_id = db.Column(db.String(36), unique=True)
    __tablename__ = 'users'

    @classmethod
    def create_user(cls, name):
        try:
            user_obj = user(name=name, user_external_id=str(uuid.uuid4()))
            db.session.add(user_obj)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            logger.error('user.create_one of name=%s and exc_class=%s, msg=%s' % name, error.__class__.__name__,
                         str(error))
            return False

class cluster(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    region = db.Column(db.String(255))
    cluster_external_id = db.Column(db.String(36), unique=True)
    user_id = db.Column(db.ForeignKey(user.id))
    user = db.relationship(user)
    CreatedAt = db.Column(db.DateTime(), nullable=False)
    ModifiedAt = db.Column(db.DateTime(), nullable=True)
    DeletedAt = db.Column(db.DateTime(), nullable=True)

    __tablename__ = 'cluster'


class machine(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    ip_addr = db.Column(db.String(255))
    instance = db.Column(db.Integer())
    threshold = db.Column(db.Integer())  # Threshold for scaling
    cluster_info_id = db.Column(db.ForeignKey(cluster.id))
    cluster_info = db.relationship(cluster)
    is_active = db.Column(db.Boolean, default=True)
    CreatedAt = db.Column(db.DateTime(), nullable=False)

    __tablename__ = 'machine'


class identifier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tag = db.Column(db.String(255))
    tagged_machine_id = db.Column(db.ForeignKey(machine.id))
    tagged_machine = db.relationship(machine)
    CreatedAt = db.Column(db.DateTime(), nullable=False)

    __tablename__ = 'identifier'