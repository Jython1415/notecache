#!/bin/bash

# This script initializes the project by creating the virtual environment and
# installing the necessary packages. It should be run from the (project) root
# directory.

python3 -m venv .venv           # Create the virtual environment
source .venv/bin/activate       # Activate the virtual environment
pip install --upgrade pip       # Update pip if necessary
pip install -r requirements.txt # Install requirements
pip install -e .                # Install package in editable mode for testing
