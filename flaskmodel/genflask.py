import os

config="""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY ='hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasktest]'
    FLASKY_MAIL_SENDER = '13285921108@163.com'
    FLASKY_ADMIN = 'huangat'
    @staticmethod
    def init_app(app):
          pass
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'mail.163.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('13285921108')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
"""
manage="""
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

#python manage.py db upgrade
"""
models="""
class User:
    pass
class Role:
    pass
"""
email="""
# -*- coding:utf-8 -*-

from threading import Thread
from email import charset
from flask_mail import Message
from flask import render_template
from flask import current_app    # 这样就不用使用from manager import app
from . import mail

charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(receiver, subject, template, **kw):
    app = current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config[
        'FLASKY_MAIL_SENDER'], recipients=[receiver], charset='utf-8')
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr
"""
init="""
# -*- coding:utf-8 -*-
from os import path
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from werkzeug.routing import BaseConverter
from config import config


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'           # login_view设置登陆页面的端点
basedir = path.abspath(path.dirname(__file__))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(
        main_blueprint, static_folder='static', template_folder='templates')

    @app.template_test('current_link')
    def current_link(link):
        return link == request.path

    return app
"""
maininit="""
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors
"""
errors="""
from flask import render_template
from . import main
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
"""
forms="""
class NameForm:
    pass
"""
views="""
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('main.index'))
    return render_template('index.html',form=form, name=session.get('name'),known=session.get('known', False),current_time=datetime.utcnow())
"""
def main():
    os.mkdir("app")
    os.mkdir("app\main")
    os.mkdir("app\static")
    os.mkdir("app\templates")
    os.mknod("app\templates\404.html")
    os.mknod("app\templates\500.html")
    os.mknod("app\templates\index.html")
    os.mkdir("tests")
    os.mkdir("venv")
    os.mkdir("migrations")
    os.mknod("requirements.txt")
    os.mknod("tests\__init__.py")
    with open("config.py","w") as f:
        f.write(config)
    with open("manage.py","w") as f:
        f.write(manage)
    with open("app\models.py","w") as f:
        f.write(models)
    with open("app\email.py","w") as f:
        f.write(email)
    with open("app\__init__.py","w") as f:
        f.write(init)
    with open("app\main\__init__.py","w") as f:
        f.write(maininit)
    with open("app\main\errors.py","w") as f:
        f.write(errors)
    with open("app\main\forms.py","w") as f:
        f.write(forms)
    with open("app\main\views.py","w") as f:
        f.write(views)

main()
