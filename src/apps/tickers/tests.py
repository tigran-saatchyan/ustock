import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

TICKER = "T"

def test_ticker_info_api(client):
    url = reverse('ticker-info', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    assert 'data' in data

def test_ticker_history_api(client):
    url = reverse('ticker-history', kwargs={'ticker': TICKER})
    params = {'start': '2022-01-01', 'end': '2022-01-10', 'interval': '1d'}
    response = client.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    assert isinstance(data.get('data'), list)

def test_ticker_dividends_api(client):
    url = reverse('ticker-dividends', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_splits_api(client):
    url = reverse('ticker-splits', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_recommendations_api(client):
    url = reverse('ticker-recommendations', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_calendar_api(client):
    url = reverse('ticker-calendar', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_sustainability_api(client):
    url = reverse('ticker-sustainability', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_holders_api(client):
    url = reverse('ticker-holders', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER

def test_ticker_news_api(client):
    url = reverse('ticker-news', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
