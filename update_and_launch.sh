#!/bin/bash

git pull
pip install -r requirements.txt
killall python3
python3 app.py --sync