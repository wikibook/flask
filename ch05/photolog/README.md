# 포토로그 : 플라스크 웹 애플리케이션

## 포토로그(photolog)

포토로그는 사진파일을 업로드하여 사진과 함께 사진에 대한 메모와 태그 위치정보들을 함께 저장하고 리스트 형태로 혹은 지도위에 보여주는 웹 어플리케이션입니다.

포토로그는 Flask 로 만들어 졌으며 SQLAlchemy, SQLite3, PIL등을 필요로 합니다.

### 설치

#### 관련된 라이브러리 설치
    pip install -r requirements.txt

#### 데이터베이스 초기화
    최초 실행시에 SQLite3 DB파일을 /photolog/resource/database/photolog 이름으로 자동 생성됨

### 애플리케이션 실행

    python runserver.py

### 사용방법
##### 1) http://localhost:5000 에 접속
##### 2) 사용자 계정을 생성
##### 3) 사진파일 업로드
##### 4) 지도에서 보기, 트윗보내기등의 기능을 사용가능

________________________

## 라이선스

[MIT license](http://opensource.org/licenses/MIT).

