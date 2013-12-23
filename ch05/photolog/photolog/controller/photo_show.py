# -*- coding: utf-8 -*-
"""
    photolog.controller.photo_show
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    업로드된 사진을 보여준다.
    
    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import request, current_app, send_from_directory \
				, render_template, session, url_for
from sqlalchemy import or_

from photolog.database import dao
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.photolog_blueprint import photolog
from photolog.photolog_logger import Log


def sizeof_fmt(num):
    """파일 사이즈를 일기 편한포맷으로 변경해주는 함수"""
    
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def get_photo_info(photolog_id):
    """업로드된 사진 관련 정보(다운로드 폴더, 파일명, 전체 파일 경로, 코멘트 등)을 얻는다.
       내부 함수인 __get_download_info()와 트위터 연동에 사용된다.
    """
    
    photo = dao.query(Photo).filter_by(id=photolog_id).first()
    download_folder = \
        os.path.join(current_app.root_path, 
                     current_app.config['UPLOAD_FOLDER'])
    download_filepath = os.path.join(download_folder, 
                                     photo.filename)
    
    return (download_folder, photo.filename, 
            download_filepath, photo.comment)


def __get_download_info(photolog_id, prefix_filename=''):
    photo_info = get_photo_info(photolog_id)
    
    download_folder = photo_info[0]
    original_filename = photo_info[1]
    download_filename = prefix_filename + original_filename

    return send_from_directory(download_folder, 
                               download_filename, 
                               as_attachment=True, 
                               mimetype='image/jpg')
    
    
@photolog.route('/photo/download/<photolog_id>')
@login_required
def download_photo(photolog_id):
    return __get_download_info(photolog_id)


@photolog.route('/photo/thumbnail/<photolog_id>')
@login_required
def download_thumbnail(photolog_id):
    return __get_download_info(photolog_id, 'thumb_')



@photolog.route('/photo/', defaults={'page': 1})
@photolog.route('/photo/page/<int:page>')
@login_required
def show_all(page=1):    
    
    user_id = session['user_info'].id
    per_page = current_app.config['PER_PAGE']
    
    photo_count = dao.query(Photo).count()
    pagination = Pagination(page, per_page, photo_count)
    
    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
    
    photo_pages = dao.query(Photo). \
                        filter_by(user_id=user_id). \
                        order_by(Photo.upload_date.desc()). \
                        limit(per_page). \
                        offset(offset). \
                        all()
    
    return render_template('list.html',
        pagination=pagination,
        photos=photo_pages,
        sizeof_fmt=sizeof_fmt) 


@photolog.route('/photo/search', methods=['POST'])
@login_required
def search_photo():    
    search_word = request.form['search_word'];
    
    if (search_word == ''):
        return show_all();
    
    user_id = session['user_info'].id
    
    photos=dao.query(Photo).filter_by(user_id=user_id). \
               filter(or_(Photo.comment.like("%" + search_word + "%"), 
                          Photo.tag.like("%" + search_word + "%"))). \
               order_by(Photo.upload_date.desc()).all()    
       
    return render_template('list.html', photos=photos, sizeof_fmt=sizeof_fmt)


@photolog.route('/photo/show/map')
@login_required
def show_map(): 
    user_id = session['user_info'].id

    return render_template('map.html', 
            photos=dao.query(Photo).
                        filter_by(user_id=user_id).
                        order_by(Photo.taken_date.desc()).all())




""" 출처 : http://flask.pocoo.org/snippets/44/ """

from math import ceil


class Pagination(object):
    
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
                
                
