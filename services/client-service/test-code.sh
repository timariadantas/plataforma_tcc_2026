#!/bin/bash

set -e
echo "Client-Service  -- Unit Tests"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found."
    echo "Create it first with:"
    echo "python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

echo "Running pytest"

pytest -v

echo "All Client Service Tests Passed!"
