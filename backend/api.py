from flask import Blueprint, request, jsonify
import json

bp = Blueprint('api', __name__, url_prefix='/text')

verses = []

try:
    with open("catechism.json") as f:
        verses = json.load(f)
except:
    print("Couldn't load Catechism")


@bp.route('/<int:index>')
def text_single(index):
    try:
        return jsonify(verses[index])
    except:
        return "Nope", 500


@bp.route('/<int:begin>/<int:end>')
def text_range(begin, end):
    try:
        return jsonify(verses[begin: end])
    except:
        return "Nope", 500
