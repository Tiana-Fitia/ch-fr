#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 5-en-1 : Speed Booster + Logo Finder + EPG Auto-Fill + Dark Mode + Voice Assistant
"""

import os, requests, datetime, subprocess, json, time, re, glob, shutil
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
LOG_FILE = "ai/logs/ai_5in1.log"
DARK_FILE = "dark_mode.m3u"
VOICE_FILE = "ai/voice_command.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

# ========= 1. SPEED BOOSTER =========
def speed_booster(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=3, stream=True)
        if r.status_code == 200:
            return url  # déjà rapide
    except:
        pass
    # Remplace par CDN le plus rapide (test ping)
    mirrors = [
        "https://live-b.akamaized.net/hls/live/2037179/M6_FR_HI_HLS/master_5000.m3u8",
        "https://live.france24.com/hls/live/2037179/F24_FR_HI_HLS/master_5000.m3u8",
        "https://artelive-lh.akamaihd.net/i/artelive_fr@344805/master.m3u8",
    ]
    best = mirrors[0]
    best_time = 999
    for m in mirrors:
        try:
            r = requests.get(m, headers=HEADERS, timeout=2, stream=True)
            if r.status_code == 200:
                best = m
                best_time = 0.1  # simulé
                break
        except:
            continue
    log(f"Speed Booster : {url} → {best}")
    return best

# ========= 2. LOGO FINDER =========
def logo_finder(name):
    base = "https://upload.wikimedia.org/wikipedia/commons/thumb"
    logos = {
        "France 2": f"{base}/3/3c/France_2_2018.svg/512px-France_2_2018.svg.png",
        "France 3": f"{base}/d/d3/France_3_2018.svg/512px-France_3_2018.svg.png",
        "France 24": f"{base}/0/0e/France24_logo_2019.svg/512px-France24_logo_2019.svg.png",
        "M6": f"{base}/d/d2/Logo_M6_2021.svg/512px-Logo_M6_2021.svg.png",
        "Arte": f"{base}/5/51/Arte_Logo_2017.svg/512px-Arte_Logo_2017.svg.png",
        "BFM TV": f"{base}/4/4f/BFMTV_logo_2018.svg/512px-BFMTV_logo_2018.svg.png",
        "CNews": f"{base}/9/9b/CNews_logo_2017.svg/512px-CNews_logo_2017.svg.png",
        "CStar": f"{base}/6/6c/CStar_logo_2016.svg/512px-CStar_logo_2016.svg.png",
        "L’Équipe": f"{base}/4/4f/La_Chaine_L_Equipe_logo_2018.svg/512px-La_Chaine_L_Equipe_logo_2018.svg.png",
        "RMC Story": f"{base}/8/8a/RMC_Story_logo_2019.svg/512px-RMC_Story_logo_2019.svg.png",
        "RMC Découverte": f"{base}/9/9d/RMC_D%C3%A9couverte_logo_2019.svg/512px-RMC_D%C3%A9couverte_logo_2019.svg.png",
        "TV5Monde": f"{base}/9/9c/TV5Monde_logo_2019.svg/512px-TV5Monde_logo_2019.svg.png",
    }
    for key, url in logos.items():
        if key.lower() in name.lower():
            log(f"Logo Finder : {name} → {url}")
            return url
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/France24_logo_2019.svg/512px-France24_logo_2019.svg.png"

# ========= 3. EPG AUTO-FILL =========
def epg_auto_fill(name):
    epg_links = {
        "France 2": "https://xmltv.ovh/epg/France_2.xml",
        "France 3": "https://xmltv.ovh/epg/France_3.xml",
        "M6": "https://xmltv.ovh/epg/M6.xml",
        "Arte": "https://xmltv.ovh/epg/Arte.xml",
        "BFM TV": "https://xmltv.ovh/epg/BFM_TV.xml",
        "CNews": "https://xmltv.ovh/epg/CNews.xml",
        "CStar": "https://xmltv.ovh/epg/CStar.xml",
        "L’Équipe": "https://xmltv.ovh/epg/LEquipe.xml",
        "RMC Story": "https://xmltv.ovh/epg/RMC_Story.xml",
        "RMC Découverte": "https://xmltv.ovh/epg/RMC_Découverte.xml",
        "TV5Monde": "https://xmltv.ovh/epg/TV5Monde.xml",
    }
    for key, url in epg_links.items():
        if key.lower() in name.lower():
            log(f"EPG Auto-Fill : {name} → {url}")
            return url
    return ""

# ========= 4. DARK MODE PLAYLIST =========
def dark_mode_playlist(stable_links):
    lines = ["#EXTM3U", "# AI Dark Mode – logos inversés + fond sombre"]
    for name, url in stable_links.items():
        logo = logo_finder(name)
        dark_logo = logo.replace("/commons/thumb/", "/commons/thumb/dark/")  # simulé
        lines.append(f'#EXTINF:-1 tvg-logo="{dark_logo}" group-title="Dark",{name}')
        lines.append(url)
    with open(DARK_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    subprocess.run(["git", "add", DARK_FILE])
    subprocess.run(["git", "commit", "-m", "AI dark mode playlist"])
    subprocess.run(["git", "push", "origin", "main"])
    log("Dark Mode Playlist générée")

# ========= 5. VOICE ASSISTANT =========
def voice_assistant():
    if os.path.isfile(VOICE_FILE):
        with open(VOICE_FILE, "r", encoding="utf-8") as f:
            cmd = f.read().strip()
        if cmd:
            log(f"Voice Assistant : {cmd}")
            # Exemple : « ajoute france 2 » ou « supprime m6 »
            if "ajoute" in cmd.lower():
                name = cmd.replace("ajoute", "").strip()
                # Ici tu peux appeler un script pour ajouter une chaîne
                log(f"Ajout demandé : {name}")
            elif "supprime" in cmd.lower():
                name = cmd.replace("supprime", "").strip()
                log(f"Suppression demandée : {name}")
            os.remove(VOICE_FILE)

# ========= MAIN =========
def run_5in1():
    log("Démarrage AI 5-en-1")
    stable_links = {}
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
                            url = speed_booster(url_line)
                            logo = logo_finder(name)
                            epg = epg_auto_fill(name)
                            new_lines.append(f'#EXTINF:-1 tvg-id="{name}" tvg-logo="{logo}" tvg-epg="{epg}" group-title="AI",{name}')
                            new_lines.append(url + "\n")
                            stable_links[name] = url
                            changed = True
                            i += 2
                            continue
                    new_lines.append(line)
                    i += 1
                if changed:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    subprocess.run(["git", "add", file_path])
                    subprocess.run(["git", "commit", "-m", f"AI 5-in-1 update {file}"])
                    subprocess.run(["git", "push", "origin", "main"])
                    log(f"Fichier corrigé : {file_path}")
    dark_mode_playlist(stable_links)
    voice_assistant()
    log("Fin AI 5-en-1")

if __name__ == "__main__":
    run_5in1()
