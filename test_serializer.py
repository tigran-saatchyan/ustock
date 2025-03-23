#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
django.setup()

# Import the serializer after Django is set up
from apps.personal_finance.serializers import AccountSerializer

# Test case 1: Valid asset (not liability, not income source)
asset_data = {
    'name': 'Test Asset',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'bank',
    'is_liability': False,
    'is_income_source': False,
    'is_cash_flow_generating': False
}

# Test case 2: Valid liability (is liability, not income source)
liability_data = {
    'name': 'Test Liability',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'mortgage',
    'is_liability': True,
    'is_income_source': False,
    'is_cash_flow_generating': False
}

# Test case 3: Valid income source (not liability, is income source)
income_data = {
    'name': 'Test Income',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'salary',
    'is_liability': False,
    'is_income_source': True,
    'is_cash_flow_generating': False
}

# Test case 4: Invalid - both liability and income source
invalid_data = {
    'name': 'Invalid Account',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'bank',
    'is_liability': True,
    'is_income_source': True,
    'is_cash_flow_generating': False
}

# Test case 5: Invalid - liability with cash flow
invalid_liability_data = {
    'name': 'Invalid Liability',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'mortgage',
    'is_liability': True,
    'is_income_source': False,
    'is_cash_flow_generating': True,
    'monthly_cash_flow': 100
}

# Test case 6: Invalid - income source with cash flow
invalid_income_data = {
    'name': 'Invalid Income',
    'balance': 1000,
    'currency': 'USD',
    'account_type': 'salary',
    'is_liability': False,
    'is_income_source': True,
    'is_cash_flow_generating': True,
    'monthly_cash_flow': 100
}

# Test each case
def test_serializer(data, case_name):
    print(f"\nTesting {case_name}:")
    print(f"Data: {data}")
    
    serializer = AccountSerializer(data=data)
    is_valid = serializer.is_valid()
    
    print(f"Is valid: {is_valid}")
    
    if not is_valid:
        print(f"Errors: {serializer.errors}")
    return is_valid

# Run all tests
print("ACCOUNT SERIALIZER VALIDATION TESTS")
print("==================================")

test_serializer(asset_data, "Valid Asset")
test_serializer(liability_data, "Valid Liability")
test_serializer(income_data, "Valid Income Source")
test_serializer(invalid_data, "Invalid - Both Liability and Income Source")
test_serializer(invalid_liability_data, "Invalid - Liability with Cash Flow")
test_serializer(invalid_income_data, "Invalid - Income Source with Cash Flow")