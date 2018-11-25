from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from model import User
class RegisterForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(1,20)])
    email=StringField('邮箱',validators=[DataRequired(),Email()])
    password=PasswordField('密码',validators=[DataRequired(),Length(1,20),EqualTo('password2')])
    password2=PasswordField('确认密码',validators=[DataRequired()])
    submit=SubmitField('注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            return False
        else:
            return True
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            return False
        else:
            return True

class LoginForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码',validators=[DataRequired(),Length(1,20)])
    remember=BooleanField('记住我')
    submit=SubmitField('登录')