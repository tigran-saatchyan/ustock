"""
Test suite for options endpoints in the UStock API.

This module tests the following endpoints:
  - Options dates endpoint ('options-dates'): returns a list of available options expiration dates.
  - Options chain endpoint ('options-chain'): returns the options chain (calls and puts) for a given ticker and expiration date.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    """Returns an instance of APIClient for testing the API endpoints."""
    return APIClient()

TICKER = "AAPL"

def test_options_dates_api(client):
    """Test the options dates endpoint.

    Sends a GET request to the 'options-dates' endpoint for the given ticker and asserts:
      - The response status is 200.
      - The response contains the expected ticker.
      - The 'data' field is a list.

    Args:
        client (APIClient): The APIClient fixture.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    url = reverse('options-dates', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    options_dates = data.get('data')
    assert isinstance(options_dates, list)

def test_options_chain_api(client):
    """Test the options chain endpoint.

    First, it retrieves the available options expiration dates via the 'options-dates' endpoint.
    If no dates are available, the test is skipped.
    Then, it sends a GET request to the 'options-chain' endpoint with a query parameter 'date'
    (using the first date from the list) and asserts:
      - The response status is 200.
      - The returned ticker matches the test ticker.
      - The 'data' field is a dictionary containing both 'calls' and 'puts'.

    Args:
        client (APIClient): The APIClient fixture.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    # Retrieve the list of options expiration dates
    dates_url = reverse('options-dates', kwargs={'ticker': TICKER})
    dates_response = client.get(dates_url)
    assert dates_response.status_code == 200
    dates_data = dates_response.json()
    options_dates = dates_data.get('data', [])
    if not options_dates:
        pytest.skip("No options dates available for ticker")
    valid_date = options_dates[0]  # use the first available date

    # Retrieve the options chain for the given ticker and date
    chain_url = reverse('options-chain', kwargs={'ticker': TICKER})
    response = client.get(chain_url, {'date': valid_date})
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    options_chain = data.get('data')
    assert isinstance(options_chain, dict)
    assert 'calls' in options_chain
    assert 'puts' in options_chain
