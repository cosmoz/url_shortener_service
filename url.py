from flask import Flask, request, redirect, abort
import redis, zlib, validators

app = Flask(__name__)
redis = redis.StrictRedis()

@app.route("/<int:key>/")
def redir(key):
    if not redis.get(key):
        abort(404)
    else:
        return redirect(redis.get(key))

@app.route("/shorten/", methods=['POST'])
def shorten():
    url = request.form['url']
    if validators.url(url):
        key = zlib.crc32(url)
        redis.set(key, url)
        return str(key)
    else:
        return 'Bad URL'

if __name__ == "__main__":
    app.run(debug=True)
