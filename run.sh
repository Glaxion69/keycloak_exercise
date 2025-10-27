#!/bin/bash

set -e


if ! command -v python &> /dev/null; then
    echo "Python not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python python-venv python-pip
fi


if [ ! -d "venv" ]; then
    python -m venv venv
fi


source venv/bin/activate
pip install -q -r requirements.txt


python generate_keycloak_stream_report.py


EXIT_CODE=$?
deactivate
exit $EXIT_CODE