#!/bin/bash

git pull
pip install -r requirements.txt
killall python
python app.py --sync