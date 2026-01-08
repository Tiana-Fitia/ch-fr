import os, json, asyncio, time, aiohttp
M3U_IN="streams/input.m3u"; M3U_OUT="streams/ch-fr.m3u8"; MAX_MS=150
async def ok(url):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as s:
            t0=time.time()
            async with s.get(url,headers={"User-Agent":"VLC"}) as r:
                lat=(time.time()-t0)*1000
                return r.status==200 and lat<=MAX_MS
    except: return False
async def main():
    with open(M3U_IN, encoding="utf-8") as f: lines=f.readlines()
    ch=[]; name=""
    for l in lines:
        l=l.strip()
        if l.startswith("#EXTINF"): name=l.split(",")[-1].strip()
        elif l and not l.startswith("#"): ch.append((name,l))
    good=[(n,u) for n,u in ch if await ok(u)]
    os.makedirs(os.path.dirname(M3U_OUT),exist_ok=True)
    with open(M3U_OUT,"w") as f:
        f.write("#EXTM3U\n")
        for n,u in good: f.write(f"#EXTINF:-1,{n}\n{u}\n")
    print(json.dumps({"valid":len(good)}))
if __name__=="__main__": asyncio.run(main())
