#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm mariadb-server mariadb-client gnome-terminal
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r Backend/requirements.txt
cd Frontend
npm install
cd ..