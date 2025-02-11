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
    # Общая информация: /api/v1/tickers/<ticker>/
    path('<str:ticker>/', TickerInfoAPIView.as_view(), name='ticker-info'),
    # Исторические данные с query параметрами: start, end, interval
    path('<str:ticker>/history/', TickerHistoryAPIView.as_view(), name='ticker-history'),
    # Дивиденды
    path('<str:ticker>/dividends/', TickerDividendsAPIView.as_view(), name='ticker-dividends'),
    # Сплиты
    path('<str:ticker>/splits/', TickerSplitsAPIView.as_view(), name='ticker-splits'),
    # Рекомендации аналитиков
    path('<str:ticker>/recommendations/', TickerRecommendationsAPIView.as_view(), name='ticker-recommendations'),
    # Календарь событий
    path('<str:ticker>/calendar/', TickerCalendarAPIView.as_view(), name='ticker-calendar'),
    # ESG данные (sustainability)
    path('<str:ticker>/sustainability/', TickerSustainabilityAPIView.as_view(), name='ticker-sustainability'),
    # Держатели (institutional, major, mutualfund)
    path('<str:ticker>/holders/', TickerHoldersAPIView.as_view(), name='ticker-holders'),
    # Новости
    path('<str:ticker>/news/', TickerNewsAPIView.as_view(), name='ticker-news'),
]
