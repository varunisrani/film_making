#!/bin/bash

# Make the script executable
chmod +x build.sh

# Set Python path for the current environment
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src:/opt/render/project/src/sd1

# Install dependencies
pip install -r requirements.txt

# Install the local package in development mode
pip install -e .

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