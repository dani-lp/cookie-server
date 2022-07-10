#!/bin/bash
source .env
source venv/bin/activate
export FLASK_APP=src.app

if [[ $1 == "--https" ]]; then
  flask run --cert=adhoc
else
  flask run
fi
