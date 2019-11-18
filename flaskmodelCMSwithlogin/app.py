from flask import Flask,render_template
from views.admin import admin_bp
from views.auth import auth_bp
from views.blog import blog_bp
from settings import config
from extensions import bootstrap,db,login_manager,csrf,ckeditor,mail,moment,toolbar,migrate
import os
from flask_wtf.csrf import CSRFError
from fakes import fake_admin, fake_categories, fake_posts, fake_comments
from flask_script import Manager
from models import Admin,Comment,Category,Post,Link
from flask_login import current_user

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
manager=Manager(app)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config[config_name])
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    register_commands(app)
    register_template_context(app)
    return app

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin=Admin.query.first()
        categories=Category.query.order_by(Category.name).all()
        links=Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments=Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments=None
        return dict(admin=admin,categories=categories,links=links,unread_comments=unread_comments)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'),400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

def register_commands(app):
    @manager.option('-d','--drop',dest='drop',default=Flask,help='create after drop.')
    def initdb(drop):
        if drop:
            db.drop_all()
            print('Drop tables')
        db.create_all()
        print('Initialized database')

    @manager.option('-u','--username', help='The username used to login.')
    @manager.option('-p','--password', help='The password used to login.')
    def init(username, password):
        print('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            print('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            print('Creating the temporary administrator account...')
            admin = Admin(username='admin', blog_title="Flaskblog", blog_sub_title="No,I am the real thing",
                          name="Miro", about="I am a fun guy....")
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            print('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        print('Done.')

    @manager.option('--category', default=10, help="Quantity of categories,default is 10")
    @manager.option('--post', default=50, help='Quantity of posts, default is 50.')
    @manager.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        db.drop_all()
        db.create_all()

        print('Generating the administrator...')
        fake_admin()

        print('Generating %d categories...' % category)
        fake_categories(category)

        print('Generating %d posts...' % post)
        fake_posts(post)

        print('Generating %d comments...' % comment)
        fake_comments(comment)

        print('Generating links...')
        #fake_links()

        print('Done.')

if __name__ == '__main__':
    create_app()
    manager.run()


