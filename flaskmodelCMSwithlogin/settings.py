import os
import sys
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())
basedir=os.path.abspath(os.path.dirname(__file__))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
    SECRET_KEY=os.getenv('SECRET_KEY','hard to guess')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=('flask blog',MAIL_USERNAME)

    FLASKBLOG_EMAIL=os.getenv('FLASKBLOG_EMAIL')
    FLASKBLOG_POST_PER_PAGE=os.getenv("FLASKBLOG_POST_PER_PAGE",10)
    FLASKBLOG_MANAGE_PER_PAGE = os.getenv("FLASKBLOG_MANAGE_PER_PAGE",15)
    FLASKBLOG_COMMENT_PER_PAGE = os.getenv("FLASKBLOG_COMMENT_PER_PAGE",15)

    FLASKBLOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    FLASKBLOG_SLOW_QUERY_THRESHOLD = 1

    FLASKBLOG_UPLOAD_PATH = os.path.join(basedir, 'upload')
    FLASKBLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=prefix + os.path.join(basedir, 'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}
