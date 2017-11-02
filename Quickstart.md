Quickstart
=====================

#### Install & run

```bash
# get repo 
git clone git@github.com:cosmoz/url_shortener_service.git
# get into dir
cd url_shortener_service
# create virtual environment for python packages isolation
virtualenv ENV
# activate venv
source ENV/bin/activate
# install requrements (flask, redis client)
pip install -e requirements.txt
# run the service
python url.py

# run redis server
redis-server
```

#### Validate service

```bash
## send request with some URL for shortcut
curl -v --data "url=https://blogs.dropbox.com/tech/2017/09/optimizing-web-servers-for-high-throughput-and-low-latency" http://localhost:5000/shorten/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /shorten/ HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 101
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 101 out of 101 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: text/html; charset=utf-8
< Content-Length: 10
< Server: Werkzeug/0.12.2 Python/2.7.14
< Date: Thu, 02 Nov 2017 16:03:09 GMT
<
* Closing connection 0
2768946887%

## let's check out does it work!
curl -v http://localhost:5000/2768946887/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /2768946887/ HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.54.0
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 302 FOUND
< Content-Type: text/html; charset=utf-8
< Content-Length: 401
< Location: https://blogs.dropbox.com/tech/2017/09/optimizing-web-servers-for-high-throughput-and-low-latency
< Server: Werkzeug/0.12.2 Python/2.7.14
< Date: Thu, 02 Nov 2017 16:03:41 GMT
<
```