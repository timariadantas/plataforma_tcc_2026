#!/bin/bash

echo "================================="
echo " RUNNING ALL SERVICES TESTS"
echo "================================="



echo "Running Client Service Tests..."

cd services/client-service || exit 1

./test-code.sh

if [ $? -ne 0 ]; then
    echo "Client Service tests failed."
    exit 1
fi



echo "Running Product Service Tests..."
cd ../product-service || exit 
./test-code.sh

if [ $? -ne 0 ]; then
    echo "Product Service tests failed."
    exit 1
fi



echo "Running Sales Service Tests..."
cd ../sales-service || exit 1

./test-code.sh

if [ $? -ne 0 ]; then
    echo "Sales Service tests failed."
    exit 1
fi



echo "================================="
echo " ALL SERVICES TESTS PASSED"
echo "================================="

exit 0