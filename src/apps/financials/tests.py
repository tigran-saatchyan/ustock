import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

TICKER = "AAPL"

def test_financials_api(client):
    url = reverse('financials', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_quarterly_financials_api(client):
    url = reverse('quarterly-financials', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_balance_sheet_api(client):
    url = reverse('balance-sheet', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_quarterly_balance_sheet_api(client):
    url = reverse('quarterly-balance-sheet', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_cashflow_api(client):
    url = reverse('cashflow', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_quarterly_cashflow_api(client):
    url = reverse('quarterly-cashflow', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_earnings_api(client):
    url = reverse('earnings', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_quarterly_earnings_api(client):
    url = reverse('quarterly-earnings', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
