from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.responses import HTMLResponse
import redis.asyncio as redis
import zlib, validators, os
from pathlib import Path

app = FastAPI()
r = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    decode_responses=True,
)
INDEX = Path(__file__).parent.joinpath('templates/index.html').read_text()


@app.get("/", response_class=HTMLResponse)
async def main():
    return INDEX


@app.get("/{key}/")
async def redir(key: int):
    url = await r.get(key)
    if url is None:
        raise HTTPException(404)
    return Response(status_code=302, headers={"Location": url})


@app.post("/shorten/")
async def shorten(url: str = Form(...)):
    if not validators.url(url):
        return Response("Bad URL", status_code=400)
    key = zlib.crc32(url.encode()) & 0xFFFFFFFF
    await r.set(key, url)
    return Response(str(key))
