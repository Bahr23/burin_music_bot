#!/bin/bash

#python3 -u /app/code/main.py
git clone https://github.com/Bahr23/burin_music_bot.git || true
cd burin_music_bot
git pull
python3 -u app/main.py