"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://{user}:{pass}@{host_params}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
