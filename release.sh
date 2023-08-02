#!/bin/bash

export PYTHONPATH="$PWD/src"
cd src
python main.py --scope="$1"
