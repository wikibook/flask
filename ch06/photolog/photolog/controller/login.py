# -*- coding: utf-8 -*-
"""
    photolog.controller.login
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    로그인 확인 데코레이터와 로그인 처리 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps
from werkzeug import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators

from photolog.database import dao
from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog
from photolog.model.user import User


@photolog.teardown_request
def close_db_session(exception=None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))


def login_required(f):
    """현재 사용자가 로그인 상태인지 확인하는 데코레이터
    로그인 상태에서 접근 가능한 함수에 적용함
    """
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_key = \
                request.cookies.get(
                    current_app.config['SESSION_COOKIE_NAME'])

            is_login = False
            if session.sid == session_key and \
                session.__contains__('user_info') :
                is_login = True

            if not is_login:
                return redirect(url_for('.login_form', 
                                        next=request.url))

            return f(*args, **kwargs)

        except Exception as e:
            Log.error("Photolog error occurs : %s" % 
                      str(e))
            raise e

    return decorated_function


@photolog.route('/')
@login_required
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return redirect(url_for('.show_all'))


@photolog.route('/user/login')
def login_form():
    """아이디/비밀번호 기반의 로그인 화면을 제공함 """
    
    next_url = request.args.get('next', '')
    regist_username = request.args.get('regist_username', '')
    update_username = request.args.get('update_username', '')
    Log.info('(%s)next_url is %s' % (request.method, next_url))
    
    form = LoginForm(request.form)

    return render_template('login.html', 
                           next_url=next_url,
                           form=form,
                           regist_username=regist_username,
                           update_username=update_username)
    
    
@photolog.route('/user/login', methods=['POST'])
def login():
    """아이디/비밀번호 기반의 로그인 기능을 제공함
    로그인 성공 시 세션에 사용자 정보를 저장하여 사용함
    """

    form = LoginForm(request.form)
    next_url = form.next_url.data
    login_error = None
    
    if form.validate():
        session.permanent = True
    
        username = form.username.data
        password = form.password.data
        next_url = form.next_url.data
        
        Log.info('(%s)next_url is %s' % (request.method, next_url))

        try:
            user = dao.query(User). \
                filter_by(username=username). \
                first()

        except Exception as e:
            Log.error(str(e))
            raise e

        if user:
            if not check_password_hash(user.password, password):
                login_error = 'Invalid password'
                
            else:
                # 세션에 추가할 정보를 session 객체의 값으로 추가함
                # 가령, User 클래스 같은 사용자 정보를 추가하는 객체 생성하고
                # 사용자 정보를 구성하여 session 객체에 추가
                session['user_info'] = user
                
                if next_url != '':
                    return redirect(next_url)
                else:
                    return redirect(url_for('.index'))
        else:
            login_error = 'User does not exist!'
            
    return render_template('login.html', 
                   next_url=next_url, 
                   error=login_error, 
                   form=form)

    
@photolog.route('/logout')
@login_required
def logout():
    """로그아웃 시에 호출되며 세션을 초기화함"""
    
    session.clear()

    return redirect(url_for('.index'))


class LoginForm(Form):
    """로그인 화면에서 사용자명과 비밀번호 입력값을 검증함"""
    
    username = \
        TextField('Username', 
                  [validators.Required('사용자명을 입력하세요.'),
                   validators.Length(
                    min=4, 
                    max=50, 
                    message='4자리 이상 50자리 이하로 입력하세요.')])
        
    password = PasswordField('New Password', 
                [validators.Required('비밀번호를 입력하세요.'),
                 validators.Length(
                    min=4, 
                    max=50, 
                    message='4자리 이상 50자리 이하로 입력하세요.')])
    
    next_url = HiddenField('Next URL')
    
