# -*- coding: utf-8 -*-
"""
    photolog.controller.twitter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    트위터와 OAUTH 연동하기 위한 모듈
    
    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import request, redirect, url_for, current_app, session
from twython import Twython, TwythonError

from photolog.controller.login import login_required
from photolog.controller.photo_show import get_photo_info
from photolog.photolog_blueprint import photolog
from photolog.photolog_logger import Log


@photolog.route('/sns/twitter/send/<photolog_id>')
@login_required
def send(photolog_id):
    """ photolog_id에 해당하는 사진과 커멘트를 트위터로 전송하는 뷰함수 """

    if (session.__contains__('TWITTER')):

        twitter = session['TWITTER']
        __send_twit(twitter, photolog_id)
            
        return redirect(url_for('.show_all'))

    else:
        # twitter 객체가 세션에 없을경우 인증단계로 이동한다.
        return __oauth(photolog_id)



def __send_twit(twitter, photolog_id):
    """ 실제로, photolog_id에 해당하는 사진과 커멘트를 트위터로 전송하는 내부 함수 """

    try:
        photo_info = get_photo_info(photolog_id)
        download_filepath = photo_info[2]
        photo_comment = photo_info[3]
        photo = open(download_filepath, 'rb')

        twitter.update_status_with_media(status=photo_comment, 
                                         media=photo)
    
        session['TWITTER_RESULT'] = 'ok' 

    except IOError as e:
        Log.error("send(): IOError , " + str(e))
        session['TWITTER_RESULT'] = str(e)

    except TwythonError as e:
        Log.error("send(): TwythonError , " + str(e))
        session['TWITTER_RESULT'] = str(e)



def __oauth(photolog_id):
    """ twitter로부터 인증토큰을 받기 위한 함수 """
    
    try:
        twitter = Twython(current_app.config['TWIT_APP_KEY'], 
                          current_app.config['TWIT_APP_SECRET'])
        
        callback_svr = current_app.config['TWIT_CALLBACK_SERVER']
        
        auth    = twitter.get_authentication_tokens(
                          callback_url= callback_svr + \
                          url_for('.callback', photolog_id=photolog_id))

        # 중간단계로 받은 임시 인증토큰은 최종인증을 위해 필요하므로 세션에 저장한다. 
        session['OAUTH_TOKEN'] = auth['oauth_token']
        session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

    except TwythonError as e:
        Log.error("__oauth(): TwythonError , "+ str(e))
        session['TWITTER_RESULT'] = str(e)

        return redirect(url_for('.show_all'))
    

    # 트위터의 사용자 권한 인증 URL로 페이지를 리다이렉트한다.
    return redirect(auth['auth_url'])




@photolog.route('/sns/twitter/callback/<photolog_id>')
@login_required
def callback(photolog_id):
    """ twitter로부터 callback url이 요청되었을때 
        최종인증을 한 후 트위터로 해당 사진과 커멘트를 전송한다.  
    """

    Log.info("callback oauth_token:" + request.args['oauth_token']);
    Log.info("callback oauth_verifier:" + request.args['oauth_verifier']);
    
    # oauth에서 twiter로 부터 넘겨받은 인증토큰을 세션으로 부터 가져온다.
    OAUTH_TOKEN        = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    oauth_verifier     = request.args['oauth_verifier']
    
    try:
        # 임시로 받은 인증토큰을 이용하여 twitter 객체를 만들고 인증토큰을 검증한다.     
        twitter = Twython(current_app.config['TWIT_APP_KEY'], 
                          current_app.config['TWIT_APP_SECRET'], 
                          OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        final_step = twitter.get_authorized_tokens(oauth_verifier)    
        
        # oauth_verifier를 통해 얻은 최종 인증토큰을 이용하여 twitter 객체를 새로 생성한다.
        twitter = Twython(current_app.config['TWIT_APP_KEY'], 
                          current_app.config['TWIT_APP_SECRET'], 
                          final_step['oauth_token'], 
                          final_step['oauth_token_secret'])
        session['TWITTER'] = twitter
    
        # 파라미터로 받은 photolog_id를 이용하여 해당 사진과 커멘트를 트위터로 전송한다.
        __send_twit(twitter, photolog_id)

    except TwythonError as e:
        Log.error("callback(): TwythonError , "+ str(e))
        session['TWITTER_RESULT'] = str(e)

    return redirect(url_for('.show_all'))

