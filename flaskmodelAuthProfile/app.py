import os

import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from auth.views import auth_bp
from user.views import user_bp
from extensions import bootstrap, db, login_manager, mail, dropzone, moment, whooshee, avatars, csrf
from auth.models import Role, User,  Permission
from settings import config
from flask_script import Manager
from main.views import main_bp

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
manager=Manager(app)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    avatars.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
def register_commands(app):
    @manager.option('-d','--drop',dest='drop',default=Flask,help='create after drop.')
    def initdb(drop):
        if drop:
            db.drop_all()
            print('Drop tables')
        db.create_all()
		Role.init_role()
        print('Initialized database')

if __name__ == '__main__':
    create_app()
    manager.run()

