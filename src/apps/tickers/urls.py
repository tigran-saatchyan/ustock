"""
URL configuration for ticker endpoints in the UStock API.

This module defines URL patterns for ticker-related endpoints, including:
  - General ticker information
  - Historical data (with query parameters: start, end, interval)
  - Dividends data
  - Stock splits data
  - Analyst recommendations
  - Event calendar data
  - ESG/Sustainability data
  - Holders information (institutional, major, mutual fund)
  - News
"""

from django.urls import path
from .views import (
    TickerInfoAPIView,
    TickerHistoryAPIView,
    TickerDividendsAPIView,
    TickerSplitsAPIView,
    TickerRecommendationsAPIView,
    TickerCalendarAPIView,
    TickerSustainabilityAPIView,
    TickerHoldersAPIView,
    TickerNewsAPIView,
)

urlpatterns = [
    # Ticker general information endpoint: /api/v1/tickers/<ticker>/
    path('<str:ticker>/', TickerInfoAPIView.as_view(), name='ticker-info'),
    # Historical data endpoint with query parameters: start, end, interval
    path('<str:ticker>/history/', TickerHistoryAPIView.as_view(), name='ticker-history'),
    # Dividends data endpoint
    path('<str:ticker>/dividends/', TickerDividendsAPIView.as_view(), name='ticker-dividends'),
    # Stock splits data endpoint
    path('<str:ticker>/splits/', TickerSplitsAPIView.as_view(), name='ticker-splits'),
    # Analyst recommendations endpoint
    path('<str:ticker>/recommendations/', TickerRecommendationsAPIView.as_view(), name='ticker-recommendations'),
    # Event calendar endpoint
    path('<str:ticker>/calendar/', TickerCalendarAPIView.as_view(), name='ticker-calendar'),
    # ESG/Sustainability data endpoint
    path('<str:ticker>/sustainability/', TickerSustainabilityAPIView.as_view(), name='ticker-sustainability'),
    # Holders information endpoint (institutional, major, mutual fund)
    path('<str:ticker>/holders/', TickerHoldersAPIView.as_view(), name='ticker-holders'),
    # News endpoint
    path('<str:ticker>/news/', TickerNewsAPIView.as_view(), name='ticker-news'),
]
