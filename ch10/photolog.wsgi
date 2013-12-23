# -*- coding: utf-8 -*-
"""
    runserver
    ~~~~~~~~~

    로컬 테스트를 위한 개발 서버 실행 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""

import sys
sys.path.insert(0,'/Users/keatonh/project/photolog')

from photolog import create_app
application = \
    create_app('/Users/keatonh/project/photolog/photolog/resource/config.cfg')      