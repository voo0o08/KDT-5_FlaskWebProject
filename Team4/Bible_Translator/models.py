## 모듈 로딩 --------------------------------------------------
from Bible_Translator import db
from datetime import datetime


## Original 테이블 클래스 -------------------------------------
## 컬럼 : id, text, create_date
class Original(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())


## Translation 테이블 클래스 ---------------------------------------
## 컬럼 : id, original_id, original, text, create_date
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_id = db.Column(
        db.Integer, db.ForeignKey("original.id", ondelete="CASCADE")
    )
    original = db.relationship("Original", backref=db.backref("translation"))
    text = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
