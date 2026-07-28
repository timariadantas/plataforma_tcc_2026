#!/bin/bash

echo "Running Product Service - Unit Tests"
if [ ! -d "venv" ]; then
    echo "Virtual environment not found."
    echo "Create it first with:"
    echo "python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

pytest app/test -v

exit $?

