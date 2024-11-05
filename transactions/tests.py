from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User, UserBankAccount, BankAccountType
from transactions.models import Transaction
from transactions.forms import DepositForm, WithdrawForm
from transactions.constants import DEPOSIT, WITHDRAWAL, INTEREST
from transactions.tasks import calculate_interest
from django.conf import settings
from decimal import Decimal
from dateutil.relativedelta import relativedelta



class TransactionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpass')
        account_type = BankAccountType.objects.create(
            name='Saving', maximum_withdrawal_amount=5000, annual_interest_rate=5.0, interest_calculation_per_year=12
        )
        self.account = UserBankAccount.objects.create(
            user=user, account_type=account_type, balance=1000.00, account_no='1234567890'
        )
        self.transaction = Transaction.objects.create(
            account=self.account, amount=100.00, transaction_type=DEPOSIT,
            balance_after_transaction=1100.00
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.account, self.account)
        self.assertEqual(self.transaction.amount, Decimal('100.00'))
        self.assertEqual(self.transaction.balance_after_transaction, Decimal('1100.00'))
        self.assertEqual(self.transaction.transaction_type, DEPOSIT)



class DepositFormTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpass')
        account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )
        self.account = UserBankAccount.objects.create(
            user=user, 
            account_type=account_type, 
            balance=1000.00,
            account_no='1234567890'  # Provide account_no field
        )
        self.min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT = 10

    def test_deposit_form_valid_data(self):
        form = DepositForm(data={'amount': 50}, account=self.account, initial={'transaction_type': DEPOSIT})
        if not form.is_valid():
            print(form.errors)  # Print the form errors if the form is invalid
        self.assertTrue(form.is_valid())

    def test_deposit_form_invalid_data(self):
        form = DepositForm(data={'amount': 5}, account=self.account, initial={'transaction_type': DEPOSIT})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], [f'You need to deposit at least {self.min_deposit_amount} $'])



class WithdrawFormTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpass')
        account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )
        self.account = UserBankAccount.objects.create(
            user=user, 
            account_type=account_type, 
            balance=1000.00,
            account_no='1234567890'  # Provide account_no field
        )
        self.min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT = 10

    def test_withdraw_form_valid_data(self):
        form = WithdrawForm(data={'amount': 50}, account=self.account, initial={'transaction_type': WITHDRAWAL})
        if not form.is_valid():
            print(form.errors)  # Print the form errors if the form is invalid
        self.assertTrue(form.is_valid())

    def test_withdraw_form_invalid_data(self):
        form = WithdrawForm(data={'amount': 5}, account=self.account, initial={'transaction_type': WITHDRAWAL})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], [f'You can withdraw at least {self.min_withdraw_amount} $'])



class TransactionViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )
        self.account = UserBankAccount.objects.create(
            user=self.user, 
            account_type=self.account_type, 
            balance=1000.00,
            account_no='1234567890'  # Provide account_no field
        )
        self.client.login(email='testuser@example.com', password='testpass')  # Login with email

    def test_deposit_money_view(self):
        response = self.client.post(reverse('transactions:deposit_money'), {
            'amount': 200, 'transaction_type': DEPOSIT,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1200.00'))

    def test_withdraw_money_view(self):
        response = self.client.post(reverse('transactions:withdraw_money'), {
            'amount': 200, 'transaction_type': WITHDRAWAL,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('800.00'))

    def test_transaction_report_view(self):
        response = self.client.get(reverse('transactions:transaction_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transaction_report.html')



class CalculateInterestTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000, 
            annual_interest_rate=5.0, 
            interest_calculation_per_year=12
        )
        # Ensuring interest_start_date aligns with the current month and interval
        current_month = timezone.now().month
        self.account = UserBankAccount.objects.create(
            user=self.user, 
            account_type=self.account_type, 
            balance=1000.00,
            initial_deposit_date=timezone.now() - relativedelta(months=12),
            interest_start_date=timezone.now() - relativedelta(months=current_month % 2 + 1),
            account_no='1234567890'  # Provide account_no field
        )

    def test_calculate_interest(self):
        calculate_interest()
        self.account.refresh_from_db()
        self.assertGreater(self.account.balance, Decimal('1000.00'))
        self.assertEqual(Transaction.objects.filter(account=self.account, transaction_type=INTEREST).count(), 1)
