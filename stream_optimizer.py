import aiohttp
import time
from predictor import predict
from config import STREAM_TIMEOUT

async def check_stream(url):
    start = time.time()
    errors = 0
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=STREAM_TIMEOUT) as resp:
                await resp.content.read(512)
    except Exception:
        errors += 1

    latency = time.time() - start
    start_time = latency

    status = predict(latency, start_time, errors)

    return {
        "latency": round(latency, 2),
        "status": ["OK", "RISQUE", "MAUVAIS"][status]
    }
