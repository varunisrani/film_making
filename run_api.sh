#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "myenv" ]; then
    source myenv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if required environment variables are set
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating a default one."
    touch .env
fi

# Set up Python path - add current directory and all subdirectories
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src:$(pwd)/sd1:$(pwd)/sd1/src:$(pwd)/agents

# Create symbolic link for sd1 package if it doesn't exist
# This helps with imports like "from sd1.src.xxx import yyy"
if [ -d "sd1" ] && [ ! -d "sd1/sd1" ]; then
    echo "Creating symbolic link for sd1 package"
    ln -sf $(pwd)/sd1 $(pwd)/sd1/sd1 || echo "Failed to create symbolic link"
fi

# Print current Python path for debugging
echo "PYTHONPATH: $PYTHONPATH"

# Get the port from environment variable or use default
PORT=${PORT:-8000}
echo "Running on port: $PORT"

# Run the FastAPI app with uvicorn
uvicorn api:app --host 0.0.0.0 --port $PORT