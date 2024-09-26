#!/bin/bash

#python3 -u /app/code/main.py
git clone https://github.com/Bahr23/burin_music_bot.git /app/src || true
cd /app/src
git pull --force
mv /app/config.py /app/src/app/.
python3 -u /app/src/app/main.py