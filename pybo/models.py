from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model): # Question 클래스는 모든 모델의 기본 클래스인 db.Model을 상속받음, db는 init파일에서 생성한 SQLAlchemy 객체
    id = db.Column(db.Integer, primary_key=True) # 각 속성은 db.Column 클래스를 사용해 생성(데이터 타입, 기본키 지정)
    subject = db.Column(db.String(200), nullable=False) # nullable=False 옵션을 지정하면 빈 값을 허용하지 않음
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) # 기존모델연결, 기존모델의 속성, 삭제연동 설정
    question = db.relationship('Question', backref=db.backref('answer_set')) # 기존모델을 참조, 참조할 모델(역참조)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


'''
ForeignKey -> 'K' 대문자 표기해야 AttributeError 해결
revision은 flask db migrate 명령을 수행할 때 무작위로 만들어 진다.
Generating /Users/Haylee/Desktop/projects/myproject/migrations/versions/fc2d5c93aaf5_.py ...  done에서 'fc2d5c93aaf5'
flaks db upgrade 명령으로 리비전파일 실행하면 데이터베이스에 모델 이름과 똑같은 question과 answer이름의 테이블이 생성된다.
pybo.db 라는 파일이 SQLite 데이터베이스의 데이터파일이 됨.
filter함수로 조회하면 리스트 형태로 반환, get함수를 사용하면 객체만 반환
db.session은 데이터베이스와 연결된 상태 의미, commit해주어야 데이터베이스에 반영
ctrl+z => flask shell 종료
'''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

