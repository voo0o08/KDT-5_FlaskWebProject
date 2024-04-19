## 모듈 로딩 --------------------------------------------------
from Bible_trans import db


## Language_eng 테이블 클래스 -------------------------------------
## 컬럼 : id, text
class Language_en(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)


## Language_ko 테이블 클래스 ---------------------------------------
## 컬럼 : id, text
class Language_ko(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)


## Language_de 테이블 클래스 ---------------------------------------
## 컬럼 : id, text
class Language_de(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)


## Language_ru 테이블 클래스 ---------------------------------------
## 컬럼 : id, text
class Language_ru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)


## Language_fr 테이블 클래스 ---------------------------------------
## 컬럼 : id, text
class Language_fr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
