#!/bin/bash

#python3 -u /app/code/main.py
git clone https://github.com/Bahr23/burin_music_bot.git /app/src || true
mv app/config.py /app/src/app/.
cd /app/src
git pull
python3 -u app/main.py