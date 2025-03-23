from rest_framework import serializers
from .models import Category, Account, Transaction, Budget, SavingsGoal


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'parent_name', 'is_expense', 'is_income', 'color', 'icon', 'subcategories']
        
    def get_subcategories(self, obj):
        # Only return direct subcategories for this category
        subcategories = obj.subcategories.all()
        if subcategories.exists():
            return CategorySerializer(subcategories, many=True, context=self.context).data
        return []


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'currency', 'account_type', 'color', 'icon', 'is_active', 
                  'is_liability', 'is_income_source', 'is_cash_flow_generating', 'monthly_cash_flow']
    
    def validate(self, data):
        """
        Custom validation to ensure that an account can't be both a liability and an income source.
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Validating account data: {data}")
        
        # Check if both flags are set
        if data.get('is_liability') and data.get('is_income_source'):
            raise serializers.ValidationError(
                {"error": "An account cannot be both a liability and an income source."}
            )
        
        # Make sure cash_flow_generating is only set for assets (not liabilities or income sources)
        if data.get('is_cash_flow_generating') and (data.get('is_liability') or data.get('is_income_source')):
            raise serializers.ValidationError(
                {"error": "Only assets can generate cash flow, not liabilities or income sources."}
            )
        
        return data


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    account_name = serializers.CharField(source='account.name', read_only=True)
    to_account_name = serializers.CharField(source='to_account.name', read_only=True, required=False)
    parent_category = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'date', 'description', 'category', 'category_name', 
                  'category_color', 'parent_category', 'account', 'account_name', 
                  'to_account', 'to_account_name', 'is_expense', 'is_income', 'is_transfer']
                  
    def get_parent_category(self, obj):
        if obj.category and obj.category.parent:
            return {
                'id': obj.category.parent.id,
                'name': obj.category.parent.name,
                'color': obj.category.parent.color
            }
        return None


class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True, allow_null=True)
    parent_category = serializers.SerializerMethodField()
    spent = serializers.SerializerMethodField()
    subcategory_budgets = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'category_color', 'category_icon', 
                  'parent_category', 'amount', 'currency', 'month', 'year', 'spent',
                  'is_parent_budget', 'parent_budget', 'subcategory_budgets']
    
    def get_parent_category(self, obj):
        if obj.category and obj.category.parent:
            return {
                'id': obj.category.parent.id,
                'name': obj.category.parent.name,
                'color': obj.category.parent.color,
                'icon': obj.category.parent.icon
            }
        return None
    
    def get_subcategory_budgets(self, obj):
        # Only return subcategory budgets if this is a parent budget
        if obj.is_parent_budget:
            subcategory_budgets = Budget.objects.filter(parent_budget=obj.id)
            if subcategory_budgets.exists():
                # Use a simple serializer to avoid infinite recursion
                return SubcategoryBudgetSerializer(subcategory_budgets, many=True, context=self.context).data
        return []
    
    def get_spent(self, obj):
        # For parent budgets, get transactions from the main category and all subcategories
        # For subcategory budgets, only get transactions for that specific subcategory
        if obj.is_parent_budget:
            # This is a parent budget, include transactions from all subcategories
            main_category = obj.category
            
            # Get all related categories (the main category and its subcategories)
            category_ids = [main_category.id]
            category_ids.extend(main_category.subcategories.values_list('id', flat=True))
            
            transactions = Transaction.objects.filter(
                user=obj.user,
                category__in=category_ids,
                is_expense=True,
                date__month=obj.month,
                date__year=obj.year
            )
        else:
            # This is a subcategory budget, only include transactions for this specific subcategory
            transactions = Transaction.objects.filter(
                user=obj.user,
                category=obj.category,
                is_expense=True,
                date__month=obj.month,
                date__year=obj.year
            )
        
        # Get transactions in the budget's currency
        same_currency_transactions = transactions.filter(account__currency=obj.currency)
        
        # Calculate total for transactions already in the budget's currency
        total_spent = sum(t.amount for t in same_currency_transactions)
        
        # Handle transactions in different currencies
        different_currency_transactions = transactions.exclude(account__currency=obj.currency)
        
        # If there are transactions in other currencies, we need to convert them
        # For now, we'll just log this situation since proper conversion would require exchange rates
        if different_currency_transactions.exists():
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Transactions in different currencies found for budget {obj.id}. "
                      f"Budget currency: {obj.currency}, Transaction currencies: "
                      f"{list(different_currency_transactions.values_list('account__currency', flat=True).distinct())}")
        
        return total_spent


class SubcategoryBudgetSerializer(serializers.ModelSerializer):
    """A simplified serializer for subcategory budgets to avoid recursion."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True, allow_null=True)
    spent = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_name', 'category_color', 'category_icon', 
                  'amount', 'currency', 'month', 'year', 'spent', 'parent_budget']
    
    def get_spent(self, obj):
        # Only include transactions for this specific subcategory
        transactions = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            is_expense=True,
            date__month=obj.month,
            date__year=obj.year
        )
        
        # Get transactions in the budget's currency
        same_currency_transactions = transactions.filter(account__currency=obj.currency)
        
        # Calculate total
        return sum(t.amount for t in same_currency_transactions)


class SavingsGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = SavingsGoal
        fields = ['id', 'name', 'target_amount', 'current_amount', 'deadline', 
                  'color', 'icon', 'is_achieved', 'progress_percentage']
    
    def get_progress_percentage(self, obj):
        if obj.target_amount == 0:
            return 0
        return round((obj.current_amount / obj.target_amount) * 100, 2)