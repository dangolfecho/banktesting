#!/bin/bash

# Run each test file
echo "Running test_login.py..."
python3 test_login.py

echo "Running test_register.py..."
python3 test_register.py

echo "Running test_deposit.py..."
python3 test_deposit.py

echo "Running test_withdraw.py..."
python3 test_withdraw.py

echo "Running test_balance.py..."
python3 test_balance.py

echo "All tests completed."
