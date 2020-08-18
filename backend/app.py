from flask import Flask, send_from_directory, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory('../frontend', filename="index.html")


@app.route('/dist/<path:path>')
def dist(path):
    print(path)
    return send_from_directory('../frontend/dist', path)


@app.route('/api/verse/<int:begin_verse>/<int:end_verse>')
def verses(begin, end):
    print(begin, end)
    return jsonify(begin, end)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
