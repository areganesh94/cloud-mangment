from app import db

instance_type = {
    'micro': 1,
    'large': 2,
}

class user(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    external_id = db.Column(db.String(36))


class cluster(db.Model):
    __tablename__ = 'cluster'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    region = db.Column(db.String(255))
    user = db.relationship('user', back_populates='cluster')


class machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    ip_addr = db.Column(db.String(255))
    instance = db.Column(db.Integer())
    threshold = db.Column(db.Integer())  # Threshold for scaling
    cluster = db.relationship('cluster', back_populates='machine')


class identifier(db.Model):
    __tablename__ = 'identfier'

    id = db.Column(db.Integer(), primary_key=True)
    tag = db.Column(db.String(255))
    user = db.relationship('machine', back_populates='identfier')
