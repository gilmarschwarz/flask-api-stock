# encoding: utf-8
from sqlalchemy.ext.hybrid import hybrid_property
from api_service.extensions import db, pwd_context

class User(db.Model):
    """Basic user model"""
    __tablename__ = 'USER'
    __table_args__ = {'schema': 'SCHEMA_NAME'}

    seq = db.Sequence('seq_user', schema="schema_name")

    id = db.Column(db.Integer, seq, server_default=seq.next_value(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def check_admin(self):
        if self.role == 'ADMIN':
            return True
        else:
            return False

    def __repr__(self):
        return "<User %s>" % self.username


class UserHistory(db.Model):
    __tablename__ = 'HISTORY'
    __table_args__ = {'schema': 'SCHEMA_NAME'}

    seq = db.Sequence('seq_hist', schema="schema_name")

    id = db.Column(db.Integer, seq, server_default=seq.next_value(), primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    date_hist = db.Column(db.DateTime, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
