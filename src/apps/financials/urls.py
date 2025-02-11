"""
URL configuration for the financials module.

This module defines URL patterns for financial endpoints in the UStock API.
The endpoints provide annual and quarterly financial data, balance sheet, cashflow,
and earnings (income statement) for a given ticker.

Endpoints:
    <str:ticker>/financials/             - Annual financial data.
    <str:ticker>/quarterly_financials/     - Quarterly financial data.
    <str:ticker>/balance_sheet/            - Annual balance sheet.
    <str:ticker>/quarterly_balance_sheet/  - Quarterly balance sheet.
    <str:ticker>/cashflow/                 - Annual cashflow data.
    <str:ticker>/quarterly_cashflow/       - Quarterly cashflow data.
    <str:ticker>/earnings/                 - Annual earnings (income statement).
    <str:ticker>/quarterly_earnings/       - Quarterly earnings (income statement).
"""

from django.urls import path
from .views import (
    FinancialsAPIView,
    QuarterlyFinancialsAPIView,
    BalanceSheetAPIView,
    QuarterlyBalanceSheetAPIView,
    CashflowAPIView,
    QuarterlyCashflowAPIView,
    EarningsAPIView,
    QuarterlyEarningsAPIView,
)

urlpatterns = [
    # Annual financial data endpoint
    path('<str:ticker>/financials/', FinancialsAPIView.as_view(), name='financials'),
    # Quarterly financial data endpoint
    path('<str:ticker>/quarterly_financials/', QuarterlyFinancialsAPIView.as_view(), name='quarterly-financials'),
    # Annual balance sheet endpoint
    path('<str:ticker>/balance_sheet/', BalanceSheetAPIView.as_view(), name='balance-sheet'),
    # Quarterly balance sheet endpoint
    path('<str:ticker>/quarterly_balance_sheet/', QuarterlyBalanceSheetAPIView.as_view(), name='quarterly-balance-sheet'),
    # Annual cashflow endpoint
    path('<str:ticker>/cashflow/', CashflowAPIView.as_view(), name='cashflow'),
    # Quarterly cashflow endpoint
    path('<str:ticker>/quarterly_cashflow/', QuarterlyCashflowAPIView.as_view(), name='quarterly-cashflow'),
    # Annual earnings (income statement) endpoint
    path('<str:ticker>/earnings/', EarningsAPIView.as_view(), name='earnings'),
    # Quarterly earnings (income statement) endpoint
    path('<str:ticker>/quarterly_earnings/', QuarterlyEarningsAPIView.as_view(), name='quarterly-earnings'),
]
