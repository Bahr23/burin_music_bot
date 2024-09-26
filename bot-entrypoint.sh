#!/bin/bash

#python3 -u /app/code/main.py
git clone https://github.com/Bahr23/burin_music_bot.git /app/src || true
git pull --force
mv /app/config.py /app/src/app/.
cd /app/src
python3 -u app/main.py