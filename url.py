from flask import Flask, redirect, abort
from lepl.apps.rfc3696 import HttpUrl
import redis, zlib

app = Flask(__name__)
redis = redis.StrictRedis()

@app.route("/<int:key>/")
def redirect(key):
    if not redis.get(key):
        abort(404)
    else:
        return redirect(redis.get(key))

@app.route("/shorten/", methods=['POST'])
def shorten():
    url = request.form['url']
    validator = HttpUrl()
    if validator(url):
        key = zlib.crc32(url)
        redis.set(key, url)
        return str(key)
    else:
        return ''

if __name__ == "__main__":
    app.run(debug=True)

