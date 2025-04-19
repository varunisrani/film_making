#!/usr/bin/env python3
"""
Script to run the Film Production AI Assistant application.
This script handles the path issues and launches the Streamlit app.
"""
import os
import sys
import subprocess

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the correct path to the Python path
sys.path.append(os.path.join(current_dir, "Users", "varunisrani", "film_making"))

# Change to the correct directory
os.chdir(os.path.join(current_dir, "Users", "varunisrani", "film_making"))

# Run the Streamlit app
subprocess.run(["streamlit", "run", "app.py"])