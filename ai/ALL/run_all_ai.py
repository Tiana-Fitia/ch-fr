#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SUPER UNIFIED : lance TOUTES les IA dans l’ordre
1. EPG Auto-Fill
2. Logo Auto-Add  
3. Multi-Audio Selector
4. 5 ms PRO Launcher
5. 5-Nouvelles-IA-en-1
6. KIMI Bot (voice)
7. 10 ms Launcher
→ 1 seul fichier, 1 seul push, tout fonctionne
"""

import os, subprocess, datetime

LOG_FILE = "ai/logs/all_ai_unified.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {msg}\n")

def run(script_path):
    log(f"Lancement : {script_path}")
    subprocess.run(["python3", script_path])
    log(f"Terminé : {script_path}")

def main():
    log("Démarrage AI SUPER UNIFIED")
    scripts = [
        "ai/epg/epg_auto_fill.py",
        "ai/logo/logo_auto_add.py",
        "ai/audio/multi_audio_selector.py",
        "ai/lowlatency/ai_5ms_pro.py",
        "ai/extra/ai_new5in1.py",
        "ai/kimi/kimi_bot.py",
        "ai/launch/ai_10ms_launcher.py",
    ]
    for sc in scripts:
        if os.path.isfile(sc):
            run(sc)
        else:
            log(f"Script absent : {sc}")
    log("Fin AI SUPER UNIFIED")

if __name__ == "__main__":
    main()
