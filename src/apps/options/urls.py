from django.urls import path
from .views import OptionsDatesAPIView, OptionsChainAPIView

urlpatterns = [
    # Даты экспираций: /api/v1/options/<ticker>/dates/
    path('<str:ticker>/dates/', OptionsDatesAPIView.as_view(), name='options-dates'),
    # Опционная цепочка для указанной даты (query параметр: ?date=YYYY-MM-DD)
    path('<str:ticker>/chain/', OptionsChainAPIView.as_view(), name='options-chain'),
]
