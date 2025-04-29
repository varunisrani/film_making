#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/storage/storyboards
mkdir -p static/storage/storyboards

# Make the script directory importable
touch agents/__init__.py
touch utils/__init__.py

# Install the local package in development mode
pip install -e .

# Set environment variables
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Install the sd1 package
cd sd1
pip install -e .
cd ..

# Print paths and environment for debugging
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo "Python path: $PYTHONPATH"
echo "Python version: $(python --version)"

echo "Build completed successfully" 