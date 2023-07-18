#!/bin/bash

pip install -r requirements-dev.txt
export PYTHONPATH="$PWD/src"
cd src
python main.py --scope="$1"
