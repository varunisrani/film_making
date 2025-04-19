#!/bin/bash

# Create proper directory structure
mkdir -p /Users/varunisrani/film_making/agents
mkdir -p /Users/varunisrani/film_making/utils
mkdir -p /Users/varunisrani/film_making/data/cache

# Move files to correct locations
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/.env.example /Users/varunisrani/film_making/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/README.md /Users/varunisrani/film_making/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/agents/* /Users/varunisrani/film_making/agents/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/utils/* /Users/varunisrani/film_making/utils/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/data/* /Users/varunisrani/film_making/data/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/app.py /Users/varunisrani/film_making/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/requirements.txt /Users/varunisrani/film_making/
mv /Users/varunisrani/film_making/Users/varunisrani/film_making/run.sh /Users/varunisrani/film_making/

# Remove empty directories
rm -rf /Users/varunisrani/film_making/Users

echo "File structure fixed!"