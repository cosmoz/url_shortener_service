from flask import Flask, request, redirect, abort, render_template
import redis, zlib, validators, os

app = Flask(__name__)
r = redis.StrictRedis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    decode_responses=True,
)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/<int:key>/")
def redir(key):
    url = r.get(key) or abort(404)
    return redirect(url)


@app.route("/shorten/", methods=['POST'])
def shorten():
    url = request.form['url']
    if not validators.url(url):
        return 'Bad URL', 400
    key = zlib.crc32(url.encode()) & 0xFFFFFFFF
    r.set(key, url)
    return str(key)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
