from extensions import mail
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template

def _send_async_mail(app,message):
    with app.app_context():
        mail.send(message)

def send_mail(to, subject, template, **kwargs):
    message = Message(subject, recipients=[to])
    #message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_confirm_email(user,token,to=None):
    send_mail(subject='KK菜谱大全--确认账号',to=to or user.email,template='mail_confirm',user=user,token=token)

def send_reset_password_email(user, token):
    send_mail(subject='KK菜谱大全--密码重置', to=user.email, template='reset_password', user=user, token=token)