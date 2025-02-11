import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

TICKER = "AAPL"

def test_options_dates_api(client):
    url = reverse('options-dates', kwargs={'ticker': TICKER})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    options_dates = data.get('data')
    assert isinstance(options_dates, list)

def test_options_chain_api(client):
    # Сначала получаем список дат экспираций
    dates_url = reverse('options-dates', kwargs={'ticker': TICKER})
    dates_response = client.get(dates_url)
    assert dates_response.status_code == 200
    dates_data = dates_response.json()
    options_dates = dates_data.get('data', [])
    if not options_dates:
        pytest.skip("No options dates available for ticker")
    valid_date = options_dates[0]  # используем первую дату
    chain_url = reverse('options-chain', kwargs={'ticker': TICKER})
    response = client.get(chain_url, {'date': valid_date})
    assert response.status_code == 200
    data = response.json()
    assert data.get('ticker') == TICKER
    options_chain = data.get('data')
    assert isinstance(options_chain, dict)
    assert 'calls' in options_chain
    assert 'puts' in options_chain
