import os, json, asyncio, time, aiohttp, numpy as np, onnxruntime as ort
M3U_IN  = "streams/input.m3u"
M3U_OUT = "streams/ch-fr.m3u8"
MAX_MS  = 150
MIN_H   = 720
async def ok(ch, name, url):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as s:
            t0 = time.perf_counter()
            async with s.get(url, headers={"User-Agent": "VLC"}) as r:
                if r.status == 200:
                    lat = (time.perf_counter() - t0) * 1000
                    probe = await asyncio.create_subprocess_exec(
                        "ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=height", "-of", "csv=p=0", url,
                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
                    stdout, _ = await probe.communicate()
                    h = int(stdout.decode().strip() or 0)
                    return lat <= MAX_MS and h >= MIN_H, h, lat
    except: pass
    return False, 0, 0
async def main():
    channels = []; name = url = ""
    with open(M3U_IN, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#EXTINF"): name = line.split(",")[-1]
            elif line and not line.startswith("#"):
                url = line; channels.append((name, url))
    results = await asyncio.gather(*(ok(*c) for c in channels))
    good = [(n, u) for (n, u), (ok, _, _) in zip(channels, results) if ok]
    os.makedirs(os.path.dirname(M3U_OUT), exist_ok=True)
    with open(M3U_OUT, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for name, url in good:
            f.write(f"#EXTINF:-1,{name}\n{url}\n")
    print(json.dumps({"valid_channels": len(good)}))
if __name__ == "__main__":
    asyncio.run(main())
