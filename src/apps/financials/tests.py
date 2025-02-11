"""
Test suite for financial endpoints in the UStock API.

This module contains tests for the following endpoints:
    - Annual financial data ('financials')
    - Quarterly financial data ('quarterly-financials')
    - Annual balance sheet ('balance-sheet')
    - Quarterly balance sheet ('quarterly-balance-sheet')
    - Annual cashflow ('cashflow')
    - Quarterly cashflow ('quarterly-cashflow')
    - Annual earnings (income statement) ('earnings')
    - Quarterly earnings (income statement) ('quarterly-earnings')

Each test sends a GET request using a test ticker ("AAPL") and verifies that:
    - The response status is 200 (OK)
    - The response contains the expected ticker symbol.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Returns an instance of APIClient for testing the API endpoints."""
    return APIClient()


TICKER = "AAPL"


def test_financials_api(client):
    """Test the annual financial data endpoint.

    Sends a GET request to the 'financials' endpoint for ticker "AAPL"
    and asserts that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('financials', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_quarterly_financials_api(client):
    """Test the quarterly financial data endpoint.

    Sends a GET request to the 'quarterly-financials' endpoint for ticker "AAPL"
    and verifies that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('quarterly-financials', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_balance_sheet_api(client):
    """Test the annual balance sheet endpoint.

    Sends a GET request to the 'balance-sheet' endpoint for ticker "AAPL"
    and asserts that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('balance-sheet', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_quarterly_balance_sheet_api(client):
    """Test the quarterly balance sheet endpoint.

    Sends a GET request to the 'quarterly-balance-sheet' endpoint for ticker "AAPL"
    and confirms that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('quarterly-balance-sheet', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_cashflow_api(client):
    """Test the annual cashflow endpoint.

    Sends a GET request to the 'cashflow' endpoint for ticker "AAPL"
    and checks that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('cashflow', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_quarterly_cashflow_api(client):
    """Test the quarterly cashflow endpoint.

    Sends a GET request to the 'quarterly-cashflow' endpoint for ticker "AAPL"
    and verifies that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('quarterly-cashflow', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_earnings_api(client):
    """Test the annual earnings endpoint.

    Sends a GET request to the 'earnings' endpoint for ticker "AAPL"
    and asserts that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('earnings', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_quarterly_earnings_api(client):
    """Test the quarterly earnings endpoint.

    Sends a GET request to the 'quarterly-earnings' endpoint for ticker "AAPL"
    and verifies that the response status is 200 and that the returned ticker is "AAPL".
    """
    url = reverse('quarterly-earnings', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
