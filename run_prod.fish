#!/usr/bin/fish

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

env FLASK_APP=main.py FLASK_ENV=production flask run -h 0.0.0.0
