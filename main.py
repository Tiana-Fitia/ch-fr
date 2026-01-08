from fastapi import FastAPI
from stream_optimizer import check_stream

app = FastAPI(title="IPTV Stream Optimizer")

@app.get("/check")
async def check(url: str):
    return await check_stream(url)
