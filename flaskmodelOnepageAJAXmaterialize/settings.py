# -*- coding: utf-8 -*-
import os
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    FLASKTODO_LOCALES = ['en_US', 'zh_Hans_CN']
    FLASKTODO_ITEM_PER_PAGE = 20

    BABEL_DEFAULT_LOCALE = FLASKTODO_LOCALES[0]

    # SERVER_NAME = 'todoism.dev:5000'  # enable subdomain support
    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
