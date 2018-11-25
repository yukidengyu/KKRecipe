from flask import request,redirect,url_for
from urllib.request import urlparse,urljoin
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import BadSignature,SignatureExpired
from settings import Operations
import os
from extensions import db
from flask import current_app

def generate_token(user,operation,expire_in=None,**kwargs):
    s=TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],expire_in)
    data={'id':user.id,'operation':operation}
    data.update(**kwargs)
    return s.dumps(data)

def validate_token(user,token,operation,new_password=None):
    s=TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    print('验证token')
    try:
        data=s.loads(token)
    except(BadSignature,SignatureExpired):
        return False
    if operation!=data.get('operation') or user.id!=data.get('id'):
        return False

    if operation==Operations.CONFIRM:
        user.confirmed=True

    elif operation==Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation==Operations.CHANGE_EMAIL:
        pass
    else:
        return False

    db.session.commit()
    return True












def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))