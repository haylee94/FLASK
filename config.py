'''
ORM을 적용하려면 config.py라는 설정 파일이 필요하다. 루트 디렉터리에 생성!
'''

import os

BASE_DIR = os.path.dirname(__file__) # 프로젝트의 루트 디렉터리

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # 데이터베이스 접속 주소
'''pybo.db라는 데이터베이스 파일을 프로젝트의 루트 디렉터리에 저장'''

SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy의 이벤트를 처리하는 옵션 -> 필요하지 않으므로 비활성화

SECRET_KEY = "dev"
