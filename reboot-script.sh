#!/bin/bash

# Detect the operating system
os_name=$(uname -s)

# Determine the venv activation command
if [[ "$os_name" == "Darwin" || "$os_name" == "Linux" ]]; then
    venv_activate="source .venv/bin/activate"
else
    echo "Unsupported operating system."
    exit 1
fi

# Activate the virtual environment
eval "$venv_activate"

# download libs to venv
pip3 install -r requirements.txt

# Run the Python script with arguments
python3 main.py "$@"

# Deactivate the virtual environment (optional)
deactivate