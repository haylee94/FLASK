from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/') # blueprint클래스로 생성한 객체(이름, 모듈명, URL프리픽스 값 전달)

'''blueprint객체 이름인 'main'은 나중에 함수명으로 URL을 찾아주는 url_for함수에서 사용 예정'''

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('question._list'))