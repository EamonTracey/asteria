#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=src

python3 src/asteria.py $@
