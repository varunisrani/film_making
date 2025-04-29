#!/bin/bash

echo "Installing packages for Film Making app..."

# Navigate to project directory
cd "$(dirname "$0")"

# Install the main package
pip install -e .

# Make sure sd1 directory has proper permissions
chmod -R 755 sd1

# Install sd1 if it has its own setup.py
if [ -f "sd1/setup.py" ]; then
    cd sd1
    pip install -e .
    cd ..
else
    # Create a temporary setup.py file for sd1 if needed
    if [ ! -f "sd1/setup.py" ]; then
        echo "Creating setup.py for sd1..."
        cat > sd1/setup.py << EOF
from setuptools import setup, find_packages

setup(
    name="sd1",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
)
EOF
        cd sd1
        pip install -e .
        cd ..
    fi
fi

echo "Setup complete. You can now run your application." 