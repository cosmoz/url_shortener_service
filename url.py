from flask import Flask, request, redirect, abort, render_template
import redis, zlib, validators, os, socket

app = Flask(__name__)
redis = redis.StrictRedis()

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/host")
def hostname():
    return socket.gethostname() 

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
        key = zlib.crc32(url) + (2**32) ## cast to unsigned int
        redis.set(key, url)
        return str(key)
    else:
        return 'Bad URL'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
