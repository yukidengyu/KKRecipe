from flask import Blueprint,render_template,url_for,redirect,flash
from flask_login import login_required,login_user,logout_user,current_user
from forms import RegisterForm,LoginForm
from model import User
from extensions import db
from settings import Operations
from mail import send_confirm_email,send_reset_password_email
from utils import generate_token,validate_token
auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        remember=form.remember.data
        user=User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            print('登录成功')
            flash('登录成功！','success')
            login_user(user=user,remember=remember)
            print(current_user)
            if current_user.confirmed:
                return redirect(url_for('main.index'))
            else:
                return render_template('confirm.html')
        else:
            flash('账号不存在或者密码错误！')
    return render_template('login.html',form=form)


@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)

        user.set_password(password)
        user.generate_email_hash()
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('邮件发送成功，请尽快确认！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html',form=form)

@auth_bp.route('/forget-password',methods=['GET','POST'])
def forget_password():
    pass

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    print('token')
    if current_user.confirmed:
        print(current_user.username)
        return redirect(url_for('main.index'))
    if validate_token(user=current_user,token=token,operation=Operations.CONFIRM):
        print('验证成功')
        flash('验证成功','success')
        return redirect(url_for('main.index'))
    else:
        print('验证失败')
        flash('验证失败','danger')
        return redirect(url_for('.resend_confirmation'))

@auth_bp.route('/profile/<username>')
@login_required
def profile(username):
    user=User.query.filter_by(username=username).first()
    return render_template('profile.html',user=user)

@auth_bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.index'))