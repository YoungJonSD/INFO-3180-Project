import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
   
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Render uses postgres://, SQLAlchemy needs postgresql://
        SQLALCHEMY_DATABASE_URI = database_url.replace('postgres://', 'postgresql://')
    else:
        # Local development fallback
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:info3180@localhost/jamdate'