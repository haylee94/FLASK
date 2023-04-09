from flask import Flask # myproject 디렉토리에서 flask run 실행
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config

'''
파일명이 app.py라면 FLASK_APP의 기본값이 app이기 때문에 flask run 실행 가능!
파일명을 기본값인 app.py가 아닌 다른 이름으로 바꾸면 Flask가 못 찾기 때문에 FLASK_APP을 실행시키길 원하는 파일명으로 설정해줘야 한다.
#window : set FLASK_APP=xxx.py
#macOS : export FLASK_APP=xxx.py
'''

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 전역변수 객체 생성 -> 다른 모듈에서도 불러서 사용하기 위해
# 함수 밖에서 객체를 생성하고 객체의 초기화는 함수 안에서 수행
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app(): # app 객체를 생성해 반환하는 함수(애플리케이션 팩토리)
    app = Flask(__name__) # __name__ 변수에 모듈명이 담긴다. 
                          # pybo.py라는 파일이 실행되면 pybo.py라는 모듈이 실행되는 것으로 __name__변수에 pybo 문자열이 담긴다. 
    '''
    @app.route('/') # 특정 주소에 접속하면 바로 다음 줄에 있는 함수를 호출하는 데코레이터
    def hello_pybo(): # app 객체가 함수안에서 사용되므로 hello_pybo 함수를 create_app 함수안에 포함
        return 'Hello, Pybo!'
    '''
    app.config.from_object(config) # config.py 작성한 항목을 app.config 환경변수로 부르기 위해 코드 추가

    # ORM
    db.init_app(app) # init_app 메서드를 이용해 초기화
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db) # init_app 메서드를 이용해 초기화
    from.import models # migrate 객체가 models.py 파일을 참조하게 함
    '''
    데이터베이스 초기화 'flask db init' 명령은 최초 한 번 수행 -> migrations 디렉터리 생성
    모델을 새로 생성하거나 변경할 때는 'flask db migrate'
    모델의 변경내용을 실제 데이터베이스에 적용할 때는 'flask db upgrade'
    '''

    # Blueprint
    from.views import main_views, question_views, answer_views, auth_views, vote_views # hello_pybo 함수 대신에 블루프린트를 사용하도록 변경
    app.register_blueprint(main_views.bp) # blueprint 객체인 bp 등록 (블루프린트를 사용하려면 생성한 블루프린트 객체를 등록)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app

