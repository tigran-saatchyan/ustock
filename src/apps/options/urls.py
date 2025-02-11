"""
URL configuration for options endpoints in the UStock API.

This module defines the following endpoints:
  - /api/v1/options/<ticker>/dates/:
      Returns the available options expiration dates for the given ticker.
  - /api/v1/options/<ticker>/chain/:
      Returns the options chain for the given ticker. It requires a query parameter "date" in the format YYYY-MM-DD.

Each endpoint is handled by a dedicated API view.
"""

from django.urls import path
from .views import OptionsDatesAPIView, OptionsChainAPIView

urlpatterns = [
    # Options expiration dates endpoint: /api/v1/options/<ticker>/dates/
    path('<str:ticker>/dates/', OptionsDatesAPIView.as_view(), name='options-dates'),
    # Options chain endpoint: /api/v1/options/<ticker>/chain/?date=YYYY-MM-DD
    path('<str:ticker>/chain/', OptionsChainAPIView.as_view(), name='options-chain'),
]
