from flask import Blueprint, request

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/verse/<int:begin_verse>/<int:end_verse>')
def verses(begin, end):
    print(begin, end)
    return jsonify(begin, end)