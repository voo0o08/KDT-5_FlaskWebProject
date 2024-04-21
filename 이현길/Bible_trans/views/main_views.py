## 모듈 로딩 --------------------------------------------------------------------------------
import pandas as pd
from flask import Blueprint, render_template, request, redirect
from Bible_trans import db
from ..models import Language_en, Language_de, Language_fr, Language_ko, Language_ru

## BP 인스턴스 생성 -------------------------------------------------------------------------
bp = Blueprint("main", __name__, template_folder="temlpates", url_prefix="/")


## 라우팅 함수들 ----------------------------------------------------------------------------
@bp.route("/")
def index():
    return "main"


@bp.route("/input")
def create_question():
    return render_template("input.html")


@bp.route("/input_data", methods=["POST"])
def input_data():
    if request.method == "POST":
        lang_text = request.form["lang_text"]

        lang_file = request.files["lang_file"]
        savepath = "Bible_trans/static/lang_files/" + lang_file.filename
        lang_file.save(savepath)
        insert_db(lang_text, savepath)

    return redirect("/")


def insert_db(lang_text, filename):
    langDB = pd.read_excel(filename, usecols=["seg"])
    for seg in langDB.values:
        lang = eval(f"Language_{lang_text}(text=seg[0])")
        db.session.add(lang)
    db.session.commit()
