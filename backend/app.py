from flask import Flask, request, json, send_from_directory
import requests
from configparser import ConfigParser
from backend import api
app = Flask(__name__)

config = ConfigParser()
config.read('config.ini')
config = config['general']


def proxy(host, path):
    response = requests.get(f"{host}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return response.content, response.status_code, headers


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def assets(path):
    if config.get("mode", False) == "development":
        return proxy(config['webpack_host'], request.path)
    return send_from_directory("../www/dist", path)


app.register_blueprint(api.bp)

