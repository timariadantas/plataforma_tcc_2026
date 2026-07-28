#!/bin/bash

echo "Sales Service - Unit Tests"

cd SalesServices.Tests || {
    echo "ERROR: Tests directory not found."
    exit 1
}

dotnet test
if [ $? -ne 0 ]; then
    echo "ERROR: Sales Service tests failed."
    exit 1
fi

echo "Sales Service tests passed."

exit 0