#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Starting build process..."

# Upgrade pip first
python -m pip install --upgrade pip

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data/storage/storyboards
mkdir -p static/storage/storyboards

# Make sure all necessary Python packages are properly structured
echo "Setting up Python packages..."
for dir in agents utils src; do
    if [ -d "$dir" ]; then
        touch "$dir/__init__.py"
        # Also create __init__.py in subdirectories
        find "$dir" -type d -exec touch {}/__init__.py \;
    fi
done

# Install the local package in development mode
echo "Installing local package..."
pip install -e .

# Set environment variables
echo "Setting up environment..."
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Move necessary files from sd1 if they exist
if [ -d "sd1/src" ]; then
    echo "Moving necessary files from sd1..."
    # Create src directory if it doesn't exist
    mkdir -p src
    # Copy files from sd1/src to src, overwriting if necessary
    cp -r sd1/src/* src/ 2>/dev/null || true
fi

# Print paths and environment for debugging
echo "Environment information:"
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la
echo "Python path: $PYTHONPATH"
echo "Python version: $(python --version)"
echo "Installed packages:"
pip list

echo "Build completed successfully" 