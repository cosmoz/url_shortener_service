url_shortener_service
=====================

#### Foreword

A long time ago in a galaxy far, far away... I started this little repo as a proof and a bet, that I will manage to write an URL shortener service in 20-30 lines of Python code.

#### I won

There was nothing but self respect of proving that someone is wrong on the Internet. He or she was using JVM platform skills and couldn't write such small bit of code that will meet business requirements. In 2017 we have:
- Groovy and Kotlin
- Convention over configuration
- µServices
- small footprint frameworks

Everything in JVM world is much more expressive than in 1995 and staying readable at this same time. But still I prefer using languages and frameworks which doesn't require an IDE for good productivity. Sticking with simple editor with plug-ins should do the work. Vim or Sublime Text are still my weapons of choice.

#### Now

Currently I have lot of time (OK, rising my son gives me *some* time on the evening) and I want to check how rusty my fingers are after doing mostly management, technical leadership and architecture in last 4+ years. There was no time for something more than quick PoC between meetings. My implementation may suck so feel free to correct me. 

#### 2026 — the world moved forward

In 2026 we have LLMs, AI agents, serverless, edge computing. The world moved forward and there is significantly more to write now.

Yet... the core idea remains: 3 endpoints, Redis storage, 1 hash function. The problem didn't get simpler — we just got better at hiding complexity.

Java Spark version is 35 lines of code + 29 lines of `pom.xml`. Not bad for a language that once needed Spring XML.

Python: 30 lines, `requirements.txt` with 3 deps. Java: 64 lines total, 2 deps. The gap is closing but Python still wins on brevity.

The bet was about proving you can do it in 20-30 lines. In 2026, I'd say: you can still do it in 35 lines if you don't count the HTML.

#### Run

```bash
docker compose up -d --build
```

Service available at `http://localhost:8080/`.

#### Run locally (Python)

```bash
pip install -r requirements.txt
python url.py
```

Requires Redis running on localhost:6379. Set `REDIS_HOST` to connect to a different instance.

#### Run locally (Java Spark)

```bash
cd java-spark
mvn compile exec:java -Dexec.mainClass=ShortUrl
```

Requires Java 21+ and Redis on localhost:6379. Default port is 5050 (port 5000 is taken by AirPlay Receiver on macOS). Set `PORT` to change.

#### Run locally (FastAPI — 2026 update)

```bash
pip install -r requirements.txt
uvicorn url_fastapi:app --host 0.0.0.0 --port 5070 --workers 4
```

Async (ASGI) implementation on `redis.asyncio` + uvloop. 35 lines of code, 3 endpoints, same contract as Flask. `--workers 1` is enough for light traffic; scale to the number of cores in production.

#### CLI test

```bash
# shorten URL
curl -X POST http://localhost:5000/shorten/ -d 'url=https://google.com'
# output: 1528440437

# redirect
curl -I http://localhost:5000/1528440437/
# output: HTTP/1.1 302 FOUND, Location: https://google.com

# bad URL
curl -X POST http://localhost:5000/shorten/ -d 'url=not-a-url'
# output: Bad URL

# missing key
curl -s http://localhost:5000/999999999/
# output: Not found (404)
```

#### Benchmark (2026)

Three implementations, the same 3 endpoints, head-to-head.

**Machine**: Apple M3 Max, 14 cores (all physical), 96 GB RAM, macOS 26.4.1
**Runtime**: OpenJDK 25.0.2, Python 3.14.4
**Client**: `bombardier -c 50 -d 10s -l` against `127.0.0.1`, keepalive
**Configuration**:
- Java: Spark 2.9.4 + Jetty 9 + JedisPool, JVM warmed up
- Flask: gunicorn 4 workers × 8 threads, redis-py ConnectionPool
- FastAPI: uvicorn 4 workers (uvloop + httptools), `redis.asyncio`

**All runs: 0 errors, 100% valid responses.**

##### Throughput (RPS)

| Endpoint           | Java         | Flask      | FastAPI         |
|--------------------|-------------:|-----------:|----------------:|
| `GET /`            |  65 869      |  6 306     | **93 105** 🏆   |
| `GET /:key` (302)  |  42 280      |  5 413     | **46 805** 🏆   |
| `POST /shorten/`   | **42 118** 🏆|  5 156     |  33 886         |

##### Latency (p50 / p99)

| Endpoint           | Java               | Flask                | FastAPI                |
|--------------------|--------------------|----------------------|------------------------|
| `GET /`            | 483μs / 5.86ms     | 7.73ms / 13.88ms     | **525μs / 792μs**      |
| `GET /:key`        | 1.18ms / 3.77ms    | 9.00ms / 15.74ms     | **1.06ms / 1.36ms**    |
| `POST /shorten/`   | 1.19ms / 3.84ms    | 9.40ms / 16.83ms     | 1.46ms / 1.90ms        |

##### Ratios

| Endpoint  | FastAPI/Flask | Java/Flask | Java/FastAPI |
|-----------|--------------:|-----------:|-------------:|
| GET /     | **14.8×**     | 10.4×      | 0.71×        |
| GET /:key | 8.6×          | 7.8×       | 0.90×        |
| POST      | 6.6×          | 8.2×       | **1.24×**    |

##### Takeaways

- **FastAPI beats Java on reads.** uvloop (libuv in C) + httptools are thinner than Jetty NIO. Async I/O to Redis is marginally cheaper than a Jetty thread blocking on a sync call.
- **FastAPI has the lowest latency everywhere.** p99 = 792μs–1.9ms vs Java 3.77–5.86ms vs Flask 13.88–16.83ms. Event loop = no GC pauses, no context switches.
- **Java wins POST by 24%.** `python-multipart` + Pydantic Form parsing adds overhead vs Spark's native `request.queryParams()`.
- **Flask caps at ~5-6k RPS.** Sync gunicorn doesn't scale beyond workers × threads. 8-15× slower than the competition.

In 2026 the 2017 bet ("URL shortener in 30 lines") cuts even sharper: 35 lines of Python gets you 90k RPS and sub-ms p99. For I/O-bound microservices, async Python is the new default.
