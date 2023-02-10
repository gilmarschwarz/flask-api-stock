# encoding: utf-8

from flask_httpauth import HTTPBasicAuth
from api_service.models import User
from passlib.hash import pbkdf2_sha256
from flask import session

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):

    user = User.query.filter_by(username=username).first()

    if user is None:
        return False

    if not pbkdf2_sha256.verify(password, user.password):
        return False

    session['id_user'] = user.id
    session['check_admin'] = user.check_admin()

    return True
