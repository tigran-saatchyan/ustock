from datetime import datetime
from django.db.models import Sum, F, Value, DecimalField, Case, When
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Category, Account, Transaction, Budget, SavingsGoal
from .serializers import (
    CategorySerializer, AccountSerializer, TransactionSerializer,
    BudgetSerializer, SavingsGoalSerializer, SubcategoryBudgetSerializer
)


class IsOwner(permissions.BasePermission):
    """Permission to only allow owners of an object to access it."""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing categories."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing accounts."""
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Creating account with data: {self.request.data}")
            serializer.save(user=self.request.user)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating account: {str(e)}")
            raise
    
    def create(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Account create method called with data: {request.data}")
        return super().create(request, *args, **kwargs)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing transactions."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-date', '-id')
        
        # Add filters
        category_id = self.request.query_params.get('category')
        account_id = self.request.query_params.get('account')
        transaction_type = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        if account_id:
            queryset = queryset.filter(account_id=account_id)
            
        if transaction_type:
            if transaction_type == 'expense':
                queryset = queryset.filter(is_expense=True)
            elif transaction_type == 'income':
                queryset = queryset.filter(is_income=True)
            elif transaction_type == 'transfer':
                queryset = queryset.filter(is_transfer=True)
                
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
            
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset
    
    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        
        # Update account balance
        account = transaction.account
        
        if transaction.is_expense:
            account.balance -= transaction.amount
        elif transaction.is_income:
            account.balance += transaction.amount
        elif transaction.is_transfer and transaction.to_account:
            # For transfers, subtract from source account and add to destination account
            account.balance -= transaction.amount
            to_account = transaction.to_account
            to_account.balance += transaction.amount
            to_account.save()
            
        account.save()


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing budgets."""
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user)
        
        # Add filters for month and year
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        only_parent = self.request.query_params.get('only_parent')
        
        if month and year:
            queryset = queryset.filter(month=month, year=year)
        elif year:
            queryset = queryset.filter(year=year)
            
        # Filter to only return parent budgets
        if only_parent and only_parent.lower() == 'true':
            queryset = queryset.filter(is_parent_budget=True)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def create_subcategory_budgets(self, request, pk=None):
        """Create multiple subcategory budgets for a parent budget."""
        parent_budget = self.get_object()
        
        # Ensure this is a parent budget
        if not parent_budget.is_parent_budget:
            return Response(
                {'error': 'This is not a parent budget'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Get subcategory budgets data from request
        subcategory_budgets_data = request.data.get('subcategory_budgets', [])
        
        if not subcategory_budgets_data:
            return Response(
                {'error': 'No subcategory budgets provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        created_budgets = []
        
        # Create each subcategory budget
        for subcategory_data in subcategory_budgets_data:
            # Make sure the category exists and belongs to the user
            category_id = subcategory_data.get('category')
            try:
                category = Category.objects.get(id=category_id, user=request.user)
            except Category.DoesNotExist:
                return Response(
                    {'error': f'Category with id {category_id} does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Create the subcategory budget
            subcategory_budget = Budget.objects.create(
                user=request.user,
                category=category,
                amount=subcategory_data.get('amount', 0),
                currency=parent_budget.currency,  # Use same currency as parent
                month=parent_budget.month,
                year=parent_budget.year,
                is_parent_budget=False,
                parent_budget=parent_budget
            )
            
            created_budgets.append(SubcategoryBudgetSerializer(subcategory_budget).data)
            
        return Response(
            {'subcategory_budgets': created_budgets},
            status=status.HTTP_201_CREATED
        )
        
    @action(detail=True, methods=['put'])
    def update_subcategory_budgets(self, request, pk=None):
        """Update multiple subcategory budgets for a parent budget."""
        parent_budget = self.get_object()
        
        # Ensure this is a parent budget
        if not parent_budget.is_parent_budget:
            return Response(
                {'error': 'This is not a parent budget'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Get subcategory budgets data from request
        subcategory_budgets_data = request.data.get('subcategory_budgets', [])
        
        if not subcategory_budgets_data:
            return Response(
                {'error': 'No subcategory budgets provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        updated_budgets = []
        created_budgets = []
        
        # Get existing subcategory budgets
        existing_budgets = Budget.objects.filter(
            parent_budget=parent_budget,
            is_parent_budget=False,
            user=request.user
        )
        
        # Create a map of category_id to budget for quick lookup
        existing_budget_map = {
            str(budget.category.id): budget for budget in existing_budgets
        }
        
        # Process each subcategory budget
        for subcategory_data in subcategory_budgets_data:
            # Make sure the category exists and belongs to the user
            category_id = subcategory_data.get('category')
            
            try:
                category = Category.objects.get(id=category_id, user=request.user)
            except Category.DoesNotExist:
                return Response(
                    {'error': f'Category with id {category_id} does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            amount = subcategory_data.get('amount', 0)
            
            # Check if this subcategory budget already exists
            if category_id in existing_budget_map:
                # Update existing budget
                budget = existing_budget_map[category_id]
                budget.amount = amount
                budget.save()
                updated_budgets.append(SubcategoryBudgetSerializer(budget).data)
            else:
                # Create new subcategory budget
                budget = Budget.objects.create(
                    user=request.user,
                    category=category,
                    amount=amount,
                    currency=parent_budget.currency,
                    month=parent_budget.month,
                    year=parent_budget.year,
                    is_parent_budget=False,
                    parent_budget=parent_budget
                )
                created_budgets.append(SubcategoryBudgetSerializer(budget).data)
            
        # Combine created and updated budgets for response
        all_budgets = updated_budgets + created_budgets
            
        return Response(
            {
                'subcategory_budgets': all_budgets,
                'updated': len(updated_budgets),
                'created': len(created_budgets)
            },
            status=status.HTTP_200_OK
        )


class SavingsGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing savings goals."""
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=True, methods=['post'])
    def add_savings(self, request, pk=None):
        goal = self.get_object()
        amount = request.data.get('amount', 0)
        
        try:
            amount = float(amount)
        except ValueError:
            return Response(
                {'error': 'Invalid amount provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        goal.current_amount += amount
        
        if goal.current_amount >= goal.target_amount:
            goal.is_achieved = True
            
        goal.save()
        
        return Response(SavingsGoalSerializer(goal).data)


class FinancialSummaryView(APIView):
    """View for getting financial summaries and reports."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get total balance across all accounts
        total_balance = Account.objects.filter(
            user=user, is_active=True
        ).aggregate(
            total=Sum('balance')
        )['total'] or 0
        
        # Get current month's income and expenses
        now = datetime.now()
        current_month_expenses = Transaction.objects.filter(
            user=user, is_expense=True, date__month=now.month, date__year=now.year
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        current_month_income = Transaction.objects.filter(
            user=user, is_income=True, date__month=now.month, date__year=now.year
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Get expense categories for current month with totals
        expense_categories = Category.objects.filter(
            user=user, is_expense=True
        )
        category_totals = []
        
        for category in expense_categories:
            total = Transaction.objects.filter(
                user=user, category=category, 
                is_expense=True, date__month=now.month, date__year=now.year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            if total > 0:
                category_totals.append({
                    'id': category.id,
                    'name': category.name,
                    'amount': total,
                    'color': category.color,
                    'icon': category.icon
                })
                
        # Sort categories by amount (descending)
        category_totals.sort(key=lambda x: x['amount'], reverse=True)
        
        # Get monthly summary for the past 6 months
        months_summary = []
        for i in range(5, -1, -1):
            month = (now.month - i) % 12
            if month == 0:
                month = 12
            year = now.year
            if now.month - i <= 0:
                year -= 1
                
            expenses = Transaction.objects.filter(
                user=user, is_expense=True,
                date__month=month, date__year=year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            income = Transaction.objects.filter(
                user=user, is_income=True,
                date__month=month, date__year=year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            months_summary.append({
                'month': month,
                'year': year,
                'expenses': expenses,
                'income': income
            })
        
        return Response({
            'total_balance': total_balance,
            'current_month_expenses': current_month_expenses,
            'current_month_income': current_month_income,
            'expense_by_category': category_totals,
            'monthly_summary': months_summary
        })