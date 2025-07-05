#!/bin/bash
#
# This script handles the setup and execution of the GitHub authentication process.

# Define the virtual environment directory
VENV_DIR="venv"

# 1. Check if the virtual environment exists. If not, create it.
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in '$VENV_DIR'..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# 2. Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# 3. Install the required packages
echo "Installing dependencies from scripts/requirements.txt..."
pip install -r scripts/requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    deactivate
    exit 1
fi

# 4. Run the Python authentication script with all provided arguments
echo "Starting the GitHub authentication process..."
python3 scripts/authenticate_github.py "$@"

# 5. Deactivate the virtual environment
deactivate
echo "Authentication process finished." 