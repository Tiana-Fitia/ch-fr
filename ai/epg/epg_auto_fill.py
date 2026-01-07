#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI EPG Auto-Fill : scan + ajoute tvg-epg depuis XMLTV officiels
"""

import os, requests, datetime, subprocess, re, xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"}
LOG_FILE = "ai/logs/epg_auto_fill.log"

# Sources XMLTV officielles et gratuites
EPG_SOURCES = {
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

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def get_epg_url(channel_name):
    for key, url in EPG_SOURCES.items():
        if key.lower() in channel_name.lower():
            return url
    return ""

def tag_epg(file_path):
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
                epg_url = get_epg_url(name)
                if epg_url:
                    new_line = line.replace('group-title="', f'tvg-epg="{epg_url}" group-title="')
                    new_lines.append(new_line)
                    new_lines.append(url_line + "\n")
                    changed = True
                    log(f"EPG ajouté : {name} → {epg_url}")
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
        subprocess.run(["git", "commit", "-m", f"AI EPG auto-fill {os.path.basename(file_path)}"])
        subprocess.run(["git", "push", "origin", "main"])
        log(f"EPG tag appliqué : {file_path}")

def run_epg_auto_fill():
    log("Démarrage AI EPG Auto-Fill")
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".m3u") and "ai" not in root:
                tag_epg(os.path.join(root, file))
    log("Fin AI EPG Auto-Fill")

if __name__ == "__main__":
    run_epg_auto_fill()
