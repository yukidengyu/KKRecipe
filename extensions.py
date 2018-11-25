from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_whooshee import Whooshee
from flask_login import LoginManager
from flask_mail import Mail
db=SQLAlchemy()
bootstrap=Bootstrap()
moment=Moment()
whooshee=Whooshee()
loginmanager=LoginManager()
mail=Mail()

@loginmanager.user_loader
def load_user(user_id):
    from model import User
    user=User.query.get(int(user_id))
    return user
loginmanager.login_view='auth.login'
loginmanager.login_message_category='warning'
loginmanager.login_message='Please log in to access this page'