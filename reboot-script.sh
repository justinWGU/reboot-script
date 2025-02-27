#!/bin/bash

BASE_DIR=$(dirname $(realpath $0))
source ${BASE_DIR}/.venv/bin/activate
python3 ${BASE_DIR}/main.py ${@}