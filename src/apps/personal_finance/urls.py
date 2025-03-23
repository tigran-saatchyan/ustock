from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, AccountViewSet, TransactionViewSet,
    BudgetViewSet, SavingsGoalViewSet, FinancialSummaryView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'savings-goals', SavingsGoalViewSet, basename='savings-goal')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', FinancialSummaryView.as_view(), name='finance-summary'),
]