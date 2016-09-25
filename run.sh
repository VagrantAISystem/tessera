#!/bin/bash

pip install -r requirements.txt 

if [[ "x$TESSERA_DEBUG" == "x" || "$TESSERA_DEBUG" == "false" ]]; then
    gunicorn --config gunicorn.conf tessera:app
else
    python run.py
fi

