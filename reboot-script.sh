#!/bin/bash

# Detect the operating system
os_name=$(uname -s)

# Determine the venv activation command
if [[ "$os_name" == "Darwin" || "$os_name" == "Linux" ]]; then
    venv_activate="source /Volumes/proj/avtr/work/jortiz/reboot-script/.venv/bin/activate"
else
    echo "Unsupported operating system."
    exit 1
fi

# Activate the virtual environment
eval "$venv_activate"

if [ "$os_name" == "Darwin" ]; then
    # download libs to venv
    pip3 install -r /Volumes/proj/avtr/work/jortiz/reboot-script/requirements.txt
    # Run the Python script with arguments
    python3 /Volumes/proj/avtr/work/jortiz/reboot-script/main.py "$@"

else
    # download libs to venv
    pip3 install -r /proj/avtr/work/jortiz/reboot-script/requirements.txt
    # Run the Python script with arguments
    python3 /proj/avtr/work/jortiz/reboot-script/main.py "$@"
fi

# Deactivate the virtual environment (optional)
deactivate