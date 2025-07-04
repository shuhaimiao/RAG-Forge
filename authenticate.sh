#!/bin/bash
#
# This script is a simple wrapper around the Python authentication script
# to make it easier to run the GitHub Copilot device authentication flow.

set -e

# Run the Python script, passing along any command-line arguments
python3 scripts/authenticate_github.py "$@" 