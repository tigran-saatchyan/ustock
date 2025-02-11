"""
Test suite for ticker endpoints in the UStock API.

This module tests the following endpoints:
    - Ticker Info: Returns general information about a ticker.
    - Ticker History: Returns historical price data with query parameters (start, end, interval).
    - Ticker Dividends: Returns dividend data.
    - Ticker Splits: Returns stock splits data.
    - Ticker Recommendations: Returns analyst recommendations.
    - Ticker Calendar: Returns event calendar data.
    - Ticker Sustainability: Returns ESG/sustainability data.
    - Ticker Holders: Returns information on institutional and major holders.
    - Ticker News: Returns news articles related to the ticker.

Each test sends a GET request to the corresponding endpoint using a test ticker ("T")
and asserts that the response status is 200 and the returned ticker matches the expected value.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    """Return an instance of APIClient for testing endpoints."""
    return APIClient()

TICKER = "T"


def test_ticker_info_api(client):
    """Test the ticker info endpoint.

    Sends a GET request to the 'ticker-info' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.
      - The response contains a 'data' key.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-info', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    assert 'data' in data


def test_ticker_history_api(client):
    """Test the ticker history endpoint.

    Sends a GET request to the 'ticker-history' endpoint with query parameters
    (start, end, interval) and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.
      - The 'data' key contains a list of historical data.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-history', kwargs={'ticker': TICKER})
    params = {'start': '2022-01-01', 'end': '2022-01-10', 'interval': '1d'}
    response = client.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    assert isinstance(data.get('data'), list)


def test_ticker_dividends_api(client):
    """Test the ticker dividends endpoint.

    Sends a GET request to the 'ticker-dividends' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-dividends', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_splits_api(client):
    """Test the ticker splits endpoint.

    Sends a GET request to the 'ticker-splits' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-splits', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_recommendations_api(client):
    """Test the ticker recommendations endpoint.

    Sends a GET request to the 'ticker-recommendations' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-recommendations', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_calendar_api(client):
    """Test the ticker calendar endpoint.

    Sends a GET request to the 'ticker-calendar' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-calendar', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_sustainability_api(client):
    """Test the ticker sustainability endpoint.

    Sends a GET request to the 'ticker-sustainability' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-sustainability', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_holders_api(client):
    """Test the ticker holders endpoint.

    Sends a GET request to the 'ticker-holders' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-holders', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER


def test_ticker_news_api(client):
    """Test the ticker news endpoint.

    Sends a GET request to the 'ticker-news' endpoint and verifies that:
      - The response status is 200.
      - The returned ticker matches the expected value.

    Args:
        client (APIClient): The APIClient fixture.
    """
    url = reverse('ticker-news', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
