#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Multi-Audio Selector : scan pistes audio FR/EN/ES/VO + tag multi-audio
"""

import os, subprocess, datetime, re, requests, json

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
LOG_FILE = "ai/logs/multi_audio.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def scan_audio_tracks(url):
    """Scan les pistes audio via requête HLS"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 200:
            return []
        lines = r.text.splitlines()
        langs = []
        for line in lines:
            if 'AUDIO' in line and ('GROUP-ID' in line or 'TYPE=AUDIO' in line):
                if 'fr' in line.lower() or 'FRE' in line or 'FRA' in line:
                    langs.append("FR")
                if 'en' in line.lower() or 'ENG' in line:
                    langs.append("EN")
                if 'es' in line.lower() or 'SPA' in line:
                    langs.append("ES")
                if 'vo' in line.lower() or 'ORIG' in line:
                    langs.append("VO")
        return list(set(langs))
    except:
        return []

def tag_multi_audio(file_path):
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
            if url_line.startswith("http"):
                name = re.search(r'tvg-id="([^"]*)"', line)
                name = name.group(1) if name else "Unknown"
                langs = scan_audio_tracks(url_line)
                if langs:
                    new_line = line.replace('group-title="', f'audio-track="{",".join(langs)}" group-title="')
                    new_lines.append(new_line)
                    new_lines.append(url_line + "\n")
                    changed = True
                    log(f"Multi-Audio : {name} → {langs}")
                else:
                    new_lines.append(line)
                    new_lines.append(url_line + "\n")
                i += 2
                continue
        new_lines.append(line)
        i += 1
    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        subprocess.run(["git", "add", file_path])
        subprocess.run(["git", "commit", "-m", f"AI Multi-Audio tag {os.path.basename(file_path)}"])
        subprocess.run(["git", "push", "origin", "main"])
        log(f"Multi-Audio tag appliqué : {file_path}")

def run_multi_audio():
    log("Démarrage AI Multi-Audio Selector")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u") and "ai" not in root:
                tag_multi_audio(os.path.join(root, file))
    log("Fin AI Multi-Audio Selector")

if __name__ == "__main__":
    run_multi_audio()
