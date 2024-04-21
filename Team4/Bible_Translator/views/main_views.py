from flask import Blueprint, render_template, request, redirect
from ..models import Translation
from Bible_Translator import db
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    translate_text = Translation.query.order_by(Translation.id.desc()).first()
    return render_template(
        "translate.html",
        translate_language=translate_text,
    )


@bp.route("/translate", methods=["POST"])
def translate():
    if request.method == "POST":
        select_language = request.form["language"]
        original_text = request.form["Content"]
        translation_text = translate_langs(select_language, original_text)
        if original_text and translation_text:
            t = Translation(
                original_text=original_text, translation_text=translation_text
            )
            db.session.add(t)
            db.session.commit()
    return redirect("/")


def translate_langs(select_language, original_text):
    curr_dir = os.getcwd()
    if select_language == "German":
        translation_text = ""
    elif select_language == "Russian":
        translation_text = ""
    elif select_language == "French":
        model_dir = curr_dir + "/Bible_Translator/static/french/results"
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        inputs = tokenizer(original_text, return_tensors="pt", padding=True)
        frenchs = model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
        )
        translation_text = tokenizer.batch_decode(frenchs, skip_special_tokens=True)[0]
    else:
        translation_text = ""

    return translation_text
