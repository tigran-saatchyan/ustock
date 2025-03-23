from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Category, Account, Transaction, Budget, SavingsGoal


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Groceries',
            user=self.user,
            is_expense=True,
            is_income=False,
            color='#e08200'
        )
        
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Groceries')
        self.assertEqual(self.category.user, self.user)
        self.assertTrue(self.category.is_expense)
        self.assertFalse(self.category.is_income)
        self.assertEqual(self.category.color, '#e08200')
        
    def test_str_representation(self):
        self.assertEqual(str(self.category), 'Groceries')


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.account = Account.objects.create(
            name='Chase Checking',
            user=self.user,
            balance=Decimal('1000.00'),
            account_type='bank'
        )
        
    def test_account_creation(self):
        self.assertEqual(self.account.name, 'Chase Checking')
        self.assertEqual(self.account.user, self.user)
        self.assertEqual(self.account.balance, Decimal('1000.00'))
        self.assertEqual(self.account.account_type, 'bank')
        
    def test_str_representation(self):
        self.assertEqual(str(self.account), 'Chase Checking')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Groceries',
            user=self.user,
            is_expense=True
        )
        self.account = Account.objects.create(
            name='Chase Checking',
            user=self.user,
            balance=Decimal('1000.00')
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            date='2023-01-01',
            description='Grocery shopping',
            category=self.category,
            account=self.account,
            is_expense=True
        )
        
    def test_transaction_creation(self):
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.amount, Decimal('50.00'))
        self.assertEqual(self.transaction.description, 'Grocery shopping')
        self.assertEqual(self.transaction.category, self.category)
        self.assertEqual(self.transaction.account, self.account)
        self.assertTrue(self.transaction.is_expense)


class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(
            name='Groceries',
            user=self.user,
            is_expense=True
        )
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('300.00'),
            month=1,
            year=2023
        )
        
    def test_budget_creation(self):
        self.assertEqual(self.budget.user, self.user)
        self.assertEqual(self.budget.category, self.category)
        self.assertEqual(self.budget.amount, Decimal('300.00'))
        self.assertEqual(self.budget.month, 1)
        self.assertEqual(self.budget.year, 2023)


class SavingsGoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.goal = SavingsGoal.objects.create(
            user=self.user,
            name='New Car',
            target_amount=Decimal('10000.00'),
            current_amount=Decimal('2000.00'),
            deadline='2023-12-31'
        )
        
    def test_savings_goal_creation(self):
        self.assertEqual(self.goal.user, self.user)
        self.assertEqual(self.goal.name, 'New Car')
        self.assertEqual(self.goal.target_amount, Decimal('10000.00'))
        self.assertEqual(self.goal.current_amount, Decimal('2000.00'))
        self.assertEqual(str(self.goal.deadline), '2023-12-31')
        self.assertFalse(self.goal.is_achieved)


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.category_data = {
            'name': 'Groceries',
            'is_expense': True,
            'is_income': False,
            'color': '#e08200'
        }
        
    def test_create_category(self):
        url = reverse('category-list')
        response = self.client.post(url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Groceries')
        
    def test_get_categories(self):
        Category.objects.create(user=self.user, **self.category_data)
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Groceries')


class AccountAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.account_data = {
            'name': 'Chase Checking',
            'balance': '1000.00',
            'account_type': 'bank',
            'currency': 'USD'
        }
        
    def test_create_account(self):
        url = reverse('account-list')
        response = self.client.post(url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'Chase Checking')
        
    def test_get_accounts(self):
        Account.objects.create(user=self.user, **self.account_data)
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Chase Checking')