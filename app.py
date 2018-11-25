
import settings
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from extensions import db,bootstrap,moment,whooshee,loginmanager,mail
from flask import Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    return app

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(admin_bp,url_prefix='/admin')
def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return 'bad request'



app=create_app()


if __name__ == '__main__':
    app.run(port=8300)
