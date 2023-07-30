#!/bin/bash

git pull
pip install -r requirements.txt
python3 app.py --sync