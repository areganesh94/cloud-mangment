import uuid
import logging
from app import db
from sqlalchemy.orm import load_only
from datetime import datetime

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
            unique_identifier = str(uuid.uuid4())
            user_obj = user(name=name, user_external_id=unique_identifier)
            db.session.add(user_obj)
            db.session.commit()
            return 'User Created successfully with unique id '+ unique_identifier+'.', 201
        except Exception as error:
            db.session.rollback()
            logger.error('user.create_one of name=%s and exc_class=%s, msg=%s' % name, error.__class__.__name__,
                         str(error))
            return "User Not created.", 503

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

    @classmethod
    def get_cluster_from_user(cls, user_id):
        try:
            user_obj = user.query.filter_by(user_external_id=user_id).options(load_only('id'))
            cluster_obj = cluster.query.filter_by(user_id=user_obj, DeletedAt=None)
            if cluster_obj:
                cluster_objs = list(cluster_obj.all())
                return [x.name for x in cluster_objs]
            else:
                return False
        except Exception as error:
            logger.error('cluster.get_cluster_from_user for user_id=%s of error=' % user_id, str(error))
            return False

    @classmethod
    def create_cluster(cls, user_id, name, region):
        try:
            user_obj = user.query.filter_by(user_external_id=user_id)
            if user_obj:
                user_obj = user_obj.first()
                cluster_unique_id = str(uuid.uuid4())
                cluster_obj = cluster(name=name, region=region, user_id=user_obj.id,
                                      cluster_external_id=cluster_unique_id, CreatedAt=datetime.now())
                db.session.add(cluster_obj)
                db.session.commit()
                return 'Cluster created with id '+cluster_unique_id+'.', 200
            else:
                return "No user found", 404
        except Exception as error:
            db.session.rollback()
            logger.error('cluster.create_cluster for user_id=%s of error=' % user_id, str(error))
            return "DB error", 503

    @classmethod
    def update_cluster_info(cls, cluster_id, name, region):
        try:
            cluster_obj = cluster.query.filter_by(cluster_external_id=cluster_id, DeletedAt=None)
            if cluster_obj.all():
                cluster_obj = cluster_obj.first()
                cluster_obj.name = name
                cluster_obj.region = region
                cluster_obj.ModifiedAt = datetime.now()
                db.session.add(cluster_obj)
                db.session.commit()
                return "Cluster updated", 200
            else:
                return "No cluster found", 404
        except Exception as error:
            db.session.rollback()
            logger.error('cluster.update_cluster_info for cluster_id=%s of error=' % cluster_id, str(error))
            return "DB error", 503

    @classmethod
    def delete_cluster(cls, cluster_id):
        try:
            cluster_obj = cluster.query.filter_by(cluster_external_id=cluster_id, DeletedAt=None).first()
            if cluster_obj:
                cluster_obj.DeletedAt = datetime.now()
                db.session.add(cluster_obj)
                db.session.commit()
                return "Cluster Deleted", 200
            else:
                return "No cluster found", 404
        except Exception as error:
            db.session.rollback()
            logger.error('cluster.delete_cluster for cluster_id=%s of error=' % cluster_id, str(error))
            return "DB error", 503


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