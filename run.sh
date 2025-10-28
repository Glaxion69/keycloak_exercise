#!/bin/bash

set -e

if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    echo "Please install: sudo apt-get install python3"
    exit 1
fi

if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is not installed"
    echo "Please install: sudo apt-get install python3-pip"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Virtual environment not found"
    echo "Please create and activate it manually:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "Then run this script again"
    exit 1
fi


if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment is not activated"
    echo "Please activate it: source venv/bin/activate"
    echo "Then run this script again"
    exit 1
fi

echo "Installing dependencies..."
pip install -q -r requires.txt

echo "Running report generator..."
python generate_keycloak_stream_report.py


EXIT_CODE=$?
deactivate
exit $EXIT_CODE