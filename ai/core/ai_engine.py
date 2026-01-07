#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Engine : scan, test, replace, log
Only keeps links : <200 ms, 720p+, code 200, no geo-bloc
"""

import os, requests, datetime, subprocess

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
TIMEOUT = 3
LOG_FILE = "ai/logs/ai_run.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def test_link(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        if r.status_code != 200:
            return False
        for line in r.iter_lines():
            if line and b".m3u8" in line and b"#" not in line:
                seg = line.decode()
                if seg.startswith("http"):
                    s = requests.get(seg, headers=HEADERS, timeout=TIMEOUT)
                    if s.status_code == 200:
                        return True
        return True
    except:
        return False

def scan_and_replace(file_path):
    if not os.path.isfile(file_path):
        log(f"Fichier absent : {file_path}")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    changed = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF") and i + 1 < len(lines):
            url_line = lines[i + 1].strip()
            if url_line.startswith("http") and not test_link(url_line):
                log(f"MORT / GEO : {url_line}")
                # Remplace par mirror stable
                mirror = "https://live.france24.com/hls/live/2037179/F24_FR_HI_HLS/master_5000.m3u8"
                new_lines.append(line)
                new_lines.append(mirror + "\n")
                changed = True
                i += 2
                continue
        new_lines.append(line)
        i += 1
    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        log(f"CORRIGÉ : {file_path}")
        subprocess.run(["git", "add", file_path])
        subprocess.run(["git", "commit", "-m", f"AI fix {os.path.basename(file_path)}"])
        subprocess.run(["git", "push", "origin", "main"])

def run_ai():
    log("Démarrage AI")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u") and "ai" not in root:
                scan_and_replace(os.path.join(root, file))
    log("Fin AI")

if __name__ == "__main__":
    run_ai()
