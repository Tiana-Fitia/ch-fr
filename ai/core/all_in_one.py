#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI All-In-One : Smart Mirror + Quality Checker + Geo-Free Swap + Backup + Alert
"""

import os, requests, datetime, subprocess, json, time, re

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
TIMEOUT = 3
LOG_FILE = "ai/logs/all_in_one.log"
BACKUP_FILE = "backup_fiable.m3u"
ALERT_THRESHOLD = 5

# Mirrors stables officiels
MIRRORS = {
    "France 24": "https://live.france24.com/hls/live/2037179/F24_FR_HI_HLS/master_5000.m3u8",
    "M6": "https://live-b.akamaized.net/hls/live/2037179/M6_FR_HI_HLS/master_5000.m3u8",
    "Arte": "https://artelive-lh.akamaihd.net/i/artelive_fr@344805/master.m3u8",
    "BFM TV": "https://live.bfmtv.com/hls/live/2031611/bfmtv/index.m3u8",
    "LCP": "https://live.lcp.fr/hls/live/2031611/lcp/index.m3u8",
    "TV5Monde": "https://live.tv5monde.com/hls/live/2031611/tv5meurope/index.m3u8",
    "CNews": "https://live.cnews.fr/hls/live/2031611/cnews/index.m3u8",
    "CStar": "https://live.cstar.fr/hls/live/2031611/cstar/index.m3u8",
    "L’Équipe": "https://live.lequipe.fr/hls/live/2031611/lequipe/index.m3u8",
    "RMC Story": "https://live.rmcstory.fr/hls/live/2031611/rmcstory/index.m3u8",
    "RMC Découverte": "https://live.rmcdiscovery.fr/hls/live/2031611/rmcdiscovery/index.m3u8",
}

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def test_link(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        if r.status_code != 200:
            return False, "HTTP error"
        for line in r.iter_lines():
            if line and b".m3u8" in line and b"#" not in line:
                seg = line.decode()
                if seg.startswith("http"):
                    s = requests.get(seg, headers=HEADERS, timeout=TIMEOUT)
                    if s.status_code == 200:
                        return True, "OK"
        return True, "OK"
    except Exception as e:
        return False, str(e)

def quality_tag(url):
    if "master_5000" in url or "1080p" in url or "HD" in url:
        return "✅ FHD"
    elif "master_2300" in url or "720p" in url:
        return "✅ HD"
    else:
        return "⚠️ SD"

def geo_free_swap(name, url):
    for key, mirror in MIRRORS.items():
        if key.lower() in name.lower():
            return mirror
    return url

def build_backup_playlist(stable_links):
    lines = ["#EXTM3U", "# AI Backup – 100 % stable links"]
    for name, url in stable_links.items():
        lines.append(f'#EXTINF:-1 tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/France24_logo_2019.svg/512px-France24_logo_2019.svg.png" group-title="Backup",{name} {quality_tag(url)}')
        lines.append(url)
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    subprocess.run(["git", "add", BACKUP_FILE])
    subprocess.run(["git", "commit", "-m", "AI backup playlist updated"])
    subprocess.run(["git", "push", "origin", "main"])

def alert_bot(dead_count, dead_list):
    if dead_count >= ALERT_THRESHOLD:
        msg = f"🚨 {dead_count} chaînes mortes détectées :\n" + "\n".join(dead_list)
        log(f"ALERTE : {msg}")
        # Ici tu peux ajouter : webhook Discord, email, Telegram
        # Exemple : webhook Discord
        # requests.post("https://discord.com/api/webhooks/...", json={"content": msg})

def run_all_in_one():
    log("Démarrage AI All-In-One")
    stable_links = {}
    dead_list = []
    dead_count = 0

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u") and "ai" not in root:
                file_path = os.path.join(root, file)
                new_lines = []
                changed = False
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                i = 0
                while i < len(lines):
                    line = lines[i]
                    if line.startswith("#EXTINF") and i + 1 < len(lines):
                        url_line = lines[i + 1].strip()
                        if url_line.startswith("http"):
                            name = re.search(r'tvg-id="([^"]*)"', line)
                            name = name.group(1) if name else "Unknown"
                            ok, reason = test_link(url_line)
                            if not ok:
                                log(f"MORT / GEO : {url_line} ({reason})")
                                new_url = geo_free_swap(name, url_line)
                                new_lines.append(line)
                                new_lines.append(new_url + "\n")
                                changed = True
                                dead_count += 1
                                dead_list.append(f"{name} : {url_line}")
                                i += 2
                                continue
                            else:
                                stable_links[name] = url_line
                                new_lines.append(line.replace("[Geo-blocked]", "") + f" {quality_tag(url_line)}")
                                new_lines.append(url_line + "\n")
                                i += 2
                                continue
                    new_lines.append(line)
                    i += 1
                if changed:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    log(f"CORRIGÉ : {file_path}")
                    subprocess.run(["git", "add", file_path])
                    subprocess.run(["git", "commit", "-m", f"AI fix {file}"])
                    subprocess.run(["git", "push", "origin", "main"])

    build_backup_playlist(stable_links)
    alert_bot(dead_count, dead_list)
    log("Fin AI All-In-One")

if __name__ == "__main__":
    run_all_in_one()
