#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Logo Auto-Add : scan + ajoute logo HD officiel pour chaque chaîne
"""

import os, requests, datetime, subprocess, re

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
LOG_FILE = "ai/logs/logo_auto_add.log"

# Logos HD officiels depuis Wikimedia Commons
LOGOS = {
    "France 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/France_2_2018.svg/512px-France_2_2018.svg.png",
    "France 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/France_3_2018.svg/512px-France_3_2018.svg.png",
    "France 4": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/France_4_2018.svg/512px-France_4_2018.svg.png",
    "France 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/France_5_2018.svg/512px-France_5_2018.svg.png",
    "France Info": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/France_Info_2017.svg/512px-France_Info_2017.svg.png",
    "M6": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Logo_M6_2021.svg/512px-Logo_M6_2021.svg.png",
    "W9": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/W9_2021.svg/512px-W9_2021.svg.png",
    "6ter": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/6ter_logo_2015.svg/512px-6ter_logo_2015.svg.png",
    "Gulli": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Gulli_logo_2017.svg/512px-Gulli_logo_2017.svg.png",
    "Arte": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Arte_Logo_2017.svg/512px-Arte_Logo_2017.svg.png",
    "BFM TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/BFMTV_logo_2018.svg/512px-BFMTV_logo_2018.svg.png",
    "BFM Business": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/BFMTV_logo_2018.svg/512px-BFMTV_logo_2018.svg.png",
    "CNews": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/CNews_logo_2017.svg/512px-CNews_logo_2017.svg.png",
    "CStar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/CStar_logo_2016.svg/512px-CStar_logo_2016.svg.png",
    "L’Équipe": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/La_Chaine_L_Equipe_logo_2018.svg/512px-La_Chaine_L_Equipe_logo_2018.svg.png",
    "LCI": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/LCI_logo_2021.svg/512px-LCI_logo_2021.svg.png",
    "RMC Story": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/RMC_Story_logo_2019.svg/512px-RMC_Story_logo_2019.svg.png",
    "RMC Découverte": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/RMC_D%C3%A9couverte_logo_2019.svg/512px-RMC_D%C3%A9couverte_logo_2019.svg.png",
    "TV5Monde": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/TV5Monde_logo_2019.svg/512px-TV5Monde_logo_2019.svg.png",
}

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def get_logo(name):
    for key, url in LOGOS.items():
        if key.lower() in name.lower():
            log(f"Logo ajouté : {name} → {url}")
            return url
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/France24_logo_2019.svg/512px-France24_logo_2019.svg.png"

def add_logo(file_path):
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
                logo = get_logo(name)
                new_line = line.replace('tvg-logo=""', f'tvg-logo="{logo}"')
                new_lines.append(new_line)
                new_lines.append(url_line + "\n")
                changed = True
                i += 2
                continue
        new_lines.append(line)
        i += 1
    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        subprocess.run(["git", "add", file_path])
        subprocess.run(["git", "commit", "-m", f"AI logo auto-add {os.path.basename(file_path)}"])
        subprocess.run(["git", "push", "origin", "main"])
        log(f"Logo appliqué : {file_path}")

def run_logo_auto_add():
    log("Démarrage AI Logo Auto-Add")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u") and "ai" not in root:
                add_logo(os.path.join(root, file))
    log("Fin AI Logo Auto-Add")

if __name__ == "__main__":
    run_logo_auto_add()
