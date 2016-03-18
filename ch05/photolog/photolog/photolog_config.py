# -*- coding: utf-8 -*-
"""
    photolog.photolog_config
    ~~~~~~~~

    photolog 디폴트 설정 모듈.
    photolog 어플리케이션에서 사용할 디폴트 설정값을 담고 있는 클래스를 정의함.

    :copyright: (c) 2013-2016 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


class PhotologConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'sqlite:///'
    #: 데이터베이스 파일 경로
    DB_FILE_PATH= 'resource/database/photolog'
    #: 사진 업로드 시 사진이 임시로 저장되는 임시 폴더
    TMP_FOLDER = 'resource/tmp/'
    #: 업로드 완료된 사진 파일이 저장되는 폴더
    UPLOAD_FOLDER = 'resource/upload/'
    #: 업로드되는 사진의 최대 크키(3메가)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'photolog_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/photolog.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    #: 트위터에 등록된 photolog 어플리케이션 인증키 (https://dev.twitter.com/)
    TWIT_APP_KEY    = '966cQr7e1mPx6Axt20uh5gwfR'
    TWIT_APP_SECRET = 'HLWQg8DtgMfnEArsnHsIX0DfetozH16vfMNh49nwH4hu1VdVH6'
    #: 트위터 연동에 대한 콜백 서버 URL(포토로그 어플리케이션 루트 경로)
    #: 로컬호스트에서 테스트를 가정하여 localhost로 설정(환경에 맞춰 변경필요) 
    TWIT_CALLBACK_SERVER = 'http://localhost:5000'
    #: 사진 목록 페이징 설정
    PER_PAGE = 10
    


