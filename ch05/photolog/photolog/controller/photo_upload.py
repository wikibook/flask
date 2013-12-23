# -*- coding: utf-8 -*-
"""
    photolog.controller.photo_upload
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    파일 업로드 모듈.
    사진을 서버의 upload 디렉토리에 저장함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import request, redirect, url_for, current_app, render_template, \
                    session
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
from PIL import Image
from wtforms import Form, FileField, TextField, TextAreaField, HiddenField, \
                    validators

from photolog.database import dao
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


def __allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photolog.route('/photo/upload')
@login_required
def upload_photo_form():
    """ 사진파일을 업로드 하기 위해 업로드폼 화면으로 전환시켜주는 함수 """
    
    form = PhotoUploadForm(request.form)
    
    return render_template('upload.html', form=form)


@photolog.route('/photo/upload', methods=['POST'])
@login_required
def upload_photo():
    """ Form으로 파일과 변수들을 DB에 저장하는 함수. """

    form = PhotoUploadForm(request.form)
        
    # HTTP POST로 요청이 오면 사용자 정보를 등록
    if form.validate():  
        #: Session에 저장된 사용자 정보를 셋팅
        user_id = session['user_info'].id
        username = session['user_info'].username
        
        
        #: Form으로 넘어온 변수들의 값을 셋팅함
        tag = form.tag.data
        comment =form.comment.data
        lat = form.lat.data
        lng = form.lng.data
        upload_date = datetime.today()
    
        try:
            #: Exif에서 전달받은 data 형식을 파이썬 date 객체로 변환
            taken_date = datetime.strptime(form.taken_date.data, 
                                           "%Y:%m:%d %H:%M:%S")
        except :
            #: date 포맷 예외 발생: exif가 없거나, 
            #: 사진찍은 시간이 없는 경우에는 현재시간으로 대체 
            taken_date = datetime.today()
        
        #: 업로드되는 파일정보 값들을 셋팅한다.
        upload_photo = request.files['photo']
        filename = None
        filesize = 0
        filename_orig = upload_photo.filename
    
        try:
            #: 파일 확장자 검사 : 현재 jpg, jpeg만 가능
            if upload_photo and __allowed_file(upload_photo.filename):
                
                ext = (upload_photo.filename).rsplit('.', 1)[1]
    
                #: 업로드 폴더 위치는 얻는다.
                upload_folder = \
                    os.path.join(current_app.root_path, 
                                 current_app.config['UPLOAD_FOLDER'])
                #: 유일하고 안전한 파일명을 얻는다.   
                filename = \
                    secure_filename(username + 
                                    '_' + 
                                    unicode(uuid.uuid4()) +
                                    "." + 
                                    ext)
                
                upload_photo.save(os.path.join(upload_folder, 
                                               filename))
                
                filesize = \
                    os.stat(upload_folder + filename).st_size
                
                #: 썸네일을 만든다.
                make_thumbnails(filename)
                
            else:
                raise Exception("File upload error : illegal file.")
    
        except Exception as e:
            Log.error(str(e))
            raise e
    
        try :
            #: 사진에 대한 정보 DB에 저장
            photo = Photo(user_id, 
                          tag, 
                          comment, 
                          filename_orig, 
                          filename, 
                          filesize, 
                          lat, lng, 
                          upload_date, 
                          taken_date)
            dao.add(photo)
            dao.commit()
    
        except Exception as e:
            dao.rollback()
            Log.error("Upload DB error : " + str(e))
            raise e
    
        return redirect(url_for('.show_all'))
    else:
        return render_template('upload.html', form=form)


@photolog.route('/photo/update/<photolog_id>', methods=['POST'])
@login_required
def update_photo(photolog_id):
    """ 사진 업로드 화면에서 사용자가 수정한 내용을 DB에 업데이트 한다. """

    form = PhotoUploadForm(request.form)

    if form.validate(): 
        #: 업데이트 대상 항목들
        tag = form.tag.data
        comment = form.comment.data
        lat = form.lat.data
        lng = form.lng.data
        
        try :
            #: 변경전 원래의 photo 테이블 값을 읽어 온다.
            photo = dao.query(Photo).filter_by(id=photolog_id).first()
            #: 업데이트 값 셋팅
            photo.tag = tag
            photo.comment = comment
            photo.geotag_lat = lat
            photo.geotag_lng = lng
            
            dao.commit()
    
        except Exception as e:
            dao.rollback()
            Log.error("Update DB error : " + str(e))
            raise e
    
        return redirect(url_for('.show_all'))
    else:
        return render_template('upload.html', photo=photo, form=form)



@photolog.route('/photo/update/<photolog_id>')
@login_required
def update_photo_form(photolog_id):
    """ 업로드폼에서 입력한 값들을 수정하기 위해 DB값을 읽어와 업로드폼 화면으로 전달한다. """
    
    photo = dao.query(Photo).filter_by(id=photolog_id).first()
    form = PhotoUploadForm(request.form, photo)
        
    return render_template('upload.html', photo=photo, form=form)



@photolog.route('/photo/remove/<photolog_id>')
@login_required
def remove(photolog_id):
    """ DB에서 해당 데이터를 삭제하고 관련된 이미지파일을 함께 삭제한다."""

    user_id = session['user_info'].id
    
    try:
        photo = dao.query(Photo).filter_by(id=str(photolog_id)).first()
        
        dao.delete(photo)
        dao.commit()

        upload_folder = os.path.join(current_app.root_path, 
                                     current_app.config['UPLOAD_FOLDER'])
        os.remove(upload_folder + str(photo.filename))
        os.remove(upload_folder + "thumb_"+str(photo.filename))

    except Exception as e:
        dao.rollback()
        Log.error("Photo remove error => " + photolog_id + ":" + user_id + \
                  ", " + str(e))
        raise e
    
    return redirect(url_for('.show_all'))


def make_thumbnails(filename):
    """ 업로드된 파일은 사이즈가 크기때문에 preview등에 사용하기 위해 
        썸네일 이미지를 생성한다.
    """
    
    upload_folder = os.path.join(current_app.root_path, 
                                 current_app.config['UPLOAD_FOLDER'])
    original_file = upload_folder+filename
    target_name = upload_folder+"thumb_"+filename
    
    try:
        #: PIL 라이브러리를 이용하여 썸네일 생성
        im = Image.open(original_file)
        im = im.convert('RGB')
        im.thumbnail((300,300), Image.ANTIALIAS)
        im.save(target_name)

    except Exception as e:
        Log.error("Thumbnails creation error : " + target_name+" , "+str(e))
        raise e

    
class PhotoUploadForm(Form):
    """사진 등록 화면에서 사진 파일, 태그, 설명 경도, 위도, 사진 찍은 날짜을 검증함"""
    
    photo = FileField('Photo')
    tag = TextField('Tag', 
                    [validators.Length(
                        min=1, 
                        max=400, 
                        message='400자리 이하로 입력하세요.')])
    comment = TextAreaField('Comment', 
                            [validators.Length(
                                min=1, 
                                max=400, 
                                message='400자리 이하로 입력하세요.')])
    lat = HiddenField('Latitude', 
                      [validators.Required(message='위치 정보(경도)가 없습니다.')])
    lng = HiddenField('Longtitude', 
                      [validators.Required(message='위도 정보(위도)가 없습니다.')])
    taken_date = HiddenField('Taken Date')
