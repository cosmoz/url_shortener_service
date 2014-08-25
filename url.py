from flask import Flask, redirect, abort
import redis, zlib

app = Flask(__name__)
redis = redis.StrictRedis()

@app.route("/<int:key>/")
def redirect(key):
    if not redis.get(key)
        abort(404)
    else:
        return redirect(target_url)

@app.route("/shorten/", methods=['POST'])
def shorten():
    url = request.form['url']
    key = zlib.crc32(url)
    redis.set(key, url)
    return str(key)

if __name__ == "__main__":
    app.run(debug=True)

