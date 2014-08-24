from flask import Flask, redirect
import redis, zlib

app = Flask(__name__)
redis = redis.StrictRedis()

@app.route("/<int:key>/")
def redirect(key):
    target_url = redis.get(key)
    return redirect(target_url)

@app.route("/shorten/", methods=['POST'])
def shorten():
    url = request.form['url']
    key = zlib.crc32(url)
    redis.set(key, url)
    return str(key)

if __name__ == "__main__":
    app.run(debug=True)

