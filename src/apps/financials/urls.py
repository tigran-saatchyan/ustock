"""
URL configuration for the financials module.

This module defines URL patterns for financial endpoints in the UStock API.
The endpoints provide annual and quarterly financial data, balance sheet, cashflow,
earnings (income statement) for a given ticker, and crypto trading functionality.

Endpoints:
    <str:ticker>/financials/             - Annual financial data.
    <str:ticker>/quarterly_financials/     - Quarterly financial data.
    <str:ticker>/balance_sheet/            - Annual balance sheet.
    <str:ticker>/quarterly_balance_sheet/  - Quarterly balance sheet.
    <str:ticker>/cashflow/                 - Annual cashflow data.
    <str:ticker>/quarterly_cashflow/       - Quarterly cashflow data.
    <str:ticker>/earnings/                 - Annual earnings (income statement).
    <str:ticker>/quarterly_earnings/       - Quarterly earnings (income statement).

    crypto/balance/                        - Crypto account balance.
    crypto/ticker/<str:symbol>/            - Crypto ticker price.
    crypto/orderbook/<str:symbol>/         - Crypto order book.
    crypto/orders/                         - Create crypto orders.
    crypto/orders/open/                    - Get open crypto orders.
    crypto/orders/<str:symbol>/<str:order_id>/ - Cancel crypto order.
    crypto/exchange/                       - Crypto exchange information.
    crypto/tickers/                        - All crypto ticker prices.
    crypto/api-keys/                       - Manage crypto API keys.
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
from .crypto_views import (
    CryptoAccountBalanceView,
    CryptoTickerPriceView,
    CryptoOrderBookView,
    CryptoCreateOrderView,
    CryptoOpenOrdersView,
    CryptoCancelOrderView,
    CryptoExchangeInfoView,
    CryptoAllTickersView,
    CryptoAPIKeysView,
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

    # Crypto trading endpoints
    path('crypto/balance/', CryptoAccountBalanceView.as_view(), name='crypto-balance'),
    path('crypto/balance/<str:exchange>/', CryptoAccountBalanceView.as_view(), name='crypto-balance-exchange'),
    path('crypto/ticker/<str:symbol>/', CryptoTickerPriceView.as_view(), name='crypto-ticker'),
    path('crypto/ticker/<str:symbol>/<str:exchange>/', CryptoTickerPriceView.as_view(), name='crypto-ticker-exchange'),
    path('crypto/orderbook/<str:symbol>/', CryptoOrderBookView.as_view(), name='crypto-orderbook'),
    path('crypto/orderbook/<str:symbol>/<str:exchange>/', CryptoOrderBookView.as_view(), name='crypto-orderbook-exchange'),
    path('crypto/orders/', CryptoCreateOrderView.as_view(), name='crypto-create-order'),
    path('crypto/orders/<str:exchange>/', CryptoCreateOrderView.as_view(), name='crypto-create-order-exchange'),
    path('crypto/orders/open/', CryptoOpenOrdersView.as_view(), name='crypto-open-orders'),
    path('crypto/orders/open/<str:exchange>/', CryptoOpenOrdersView.as_view(), name='crypto-open-orders-exchange'),
    path('crypto/orders/<str:symbol>/<str:order_id>/', CryptoCancelOrderView.as_view(), name='crypto-cancel-order'),
    path('crypto/orders/<str:symbol>/<str:order_id>/<str:exchange>/', CryptoCancelOrderView.as_view(), name='crypto-cancel-order-exchange'),
    path('crypto/exchange/', CryptoExchangeInfoView.as_view(), name='crypto-exchange-info'),
    path('crypto/exchange/<str:exchange>/', CryptoExchangeInfoView.as_view(), name='crypto-exchange-info-exchange'),
    path('crypto/tickers/', CryptoAllTickersView.as_view(), name='crypto-all-tickers'),
    path('crypto/tickers/<str:exchange>/', CryptoAllTickersView.as_view(), name='crypto-all-tickers-exchange'),
    path('crypto/api-keys/', CryptoAPIKeysView.as_view(), name='crypto-api-keys'),
    path('crypto/api-keys/<str:exchange>/', CryptoAPIKeysView.as_view(), name='crypto-api-keys-exchange'),
]
