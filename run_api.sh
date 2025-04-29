#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "myenv" ]; then
    source myenv/bin/activate
fi

# Check if required environment variables are set
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating a default one."
    touch .env
fi

# Set up Python path
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src:$(pwd)/sd1:$(pwd)/sd1/src:$(pwd)/agents

# Run the FastAPI app with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000 --reload