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
    path('<str:ticker>/financials/', FinancialsAPIView.as_view(), name='financials'),
    path('<str:ticker>/quarterly_financials/', QuarterlyFinancialsAPIView.as_view(), name='quarterly-financials'),
    path('<str:ticker>/balance_sheet/', BalanceSheetAPIView.as_view(), name='balance-sheet'),
    path('<str:ticker>/quarterly_balance_sheet/', QuarterlyBalanceSheetAPIView.as_view(), name='quarterly-balance-sheet'),
    path('<str:ticker>/cashflow/', CashflowAPIView.as_view(), name='cashflow'),
    path('<str:ticker>/quarterly_cashflow/', QuarterlyCashflowAPIView.as_view(), name='quarterly-cashflow'),
    path('<str:ticker>/earnings/', EarningsAPIView.as_view(), name='earnings'),
    path('<str:ticker>/quarterly_earnings/', QuarterlyEarningsAPIView.as_view(), name='quarterly-earnings'),
]
