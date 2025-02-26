#!/bin/bash

BASE_DIR=$(dirname $(realpath $0))
source ${BASE_DIR}/.venv/bin/activate
python ${BASE_DIR}/main.py ${@}
