#!/bin/bash

#python3 -u /app/code/main.py
git clone https://github.com/Bahr23/burin_music_bot.git /app/src || true
cd /app/src/burin_music_bot
git pull --force
mv /app/config.py /app/src/app/.
python3 -u /app/app/main.py