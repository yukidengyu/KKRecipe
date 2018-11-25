from extensions import db
from extensions import whooshee
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import hashlib
from datetime import datetime
@whooshee.register_model('name','ingredient')
class Recipe(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.String(10))
    name=db.Column(db.String(30))
    ingredient=db.Column(db.String(200))
    imageurl=db.Column(db.Text)
    t=db.Column(db.String(20))
    author=db.relationship('User',back_populates='recipes')

class User(UserMixin,db.Model):
    @property
    def gravatar(self):
        return 'https://gravatar.com/avatar/%s?d=monsterid' % self.email_hash
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30))
    email = db.Column(db.String(254), unique=True, nullable=False)
    email_hash = db.Column(db.String(128))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)
    recipe_id=db.Column(db.Integer,db.ForeignKey('recipe.id'))
    recipes=db.relationship('Recipe',back_populates='author')

    def generate_email_hash(self):
        if self.email is not None and self.email_hash is None:
            self.email_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def validate_password(self,password):
        if check_password_hash(self.password_hash,password):
            return True
        else:
            return False
