from django.test import TestCase  # Imports Django's testing framework for writing tests
from django.urls import reverse  # Helps in generating URLs from view names
from django.utils import timezone  # Provides timezone-aware date/time functions
from accounts.models import User, UserBankAccount, BankAccountType  # Imports models for user and bank accounts
from transactions.models import Transaction  # Imports the Transaction model
from transactions.forms import DepositForm, WithdrawForm  # Imports forms for deposit and withdrawal actions
from transactions.constants import DEPOSIT, WITHDRAWAL, INTEREST  # Imports constants for transaction types
from transactions.tasks import calculate_interest  # Imports task function for calculating interest
from django.conf import settings  # Accesses project settings
from decimal import Decimal  # Provides precise decimal arithmetic
from dateutil.relativedelta import relativedelta  # Allows date manipulation by specific time intervals

class TransactionModelTest(TestCase):  # Defines tests for the Transaction model
    def setUp(self):  # Setup function runs before each test
        # Creates a test user and securely hashes the password before saving it to the database
        user = User.objects.create_user(email='testuser@example.com', password='testpass')
        account_type = BankAccountType.objects.create(
            name='Saving', maximum_withdrawal_amount=5000, annual_interest_rate=5.0, interest_calculation_per_year=12
        )  # Creates a "Saving" account type with specified limits and interest rate
        self.account = UserBankAccount.objects.create(
            user=user, account_type=account_type, balance=1000.00, account_no='1234567890'
        )  # Creates a bank account for the user
        self.transaction = Transaction.objects.create(
            account=self.account, amount=100.00, transaction_type=DEPOSIT,
            balance_after_transaction=1100.00
        )  # Creates a deposit transaction

    def test_transaction_creation(self):  # Tests if transaction details are correct
        self.assertEqual(self.transaction.account, self.account)  # Checks if transaction's account matches
        self.assertEqual(self.transaction.amount, Decimal('100.00'))  # Confirms transaction amount is correct
        self.assertEqual(self.transaction.balance_after_transaction, Decimal('1100.00'))  # Checks resulting balance
        self.assertEqual(self.transaction.transaction_type, DEPOSIT)  # Verifies transaction type is DEPOSIT

class DepositFormTest(TestCase):  # Defines tests for DepositForm
    def setUp(self):  # Sets up a test account and minimum deposit amount
        user = User.objects.create_user(email='testuser@example.com', password='testpass')  # Creates a test user
        account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )  # Creates a "Saving" account type with specific limits
        self.account = UserBankAccount.objects.create(
            user=user, 
            account_type=account_type, 
            balance=1000.00,
            account_no='1234567890'
        )  # Creates a bank account for the user
        self.min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT = 10  # Sets minimum deposit amount to 10

    def test_deposit_form_valid_data(self):  # Tests deposit form with valid data
        # The `initial` dictionary sets default values for certain form fields 
        # (e.g., 'transaction_type') that are pre-populated when the form is rendered or used
        form = DepositForm(data={'amount': 50}, account=self.account, initial={'transaction_type': DEPOSIT})
        if not form.is_valid():
            print(form.errors)  # Prints form errors if invalid
        self.assertTrue(form.is_valid())  # Asserts form is valid with the given data
        # form.is_valid() ->  Returns a boolean indicating if the form data passes validation checks (True if valid, False otherwise)
        # form.errors ->  Returns a dictionary containing field-specific validation errors with lists of error messages as values

    def test_deposit_form_invalid_data(self):  # Tests deposit form with invalid data
        form = DepositForm(data={'amount': 5}, account=self.account, initial={'transaction_type': DEPOSIT})
        self.assertFalse(form.is_valid())  # Checks form is invalid
        self.assertEqual(form.errors['amount'], [f'You need to deposit at least {self.min_deposit_amount} $'])  # Checks error message
        
    def test_deposit_without_login(self):
        self.client.logout()
        response = self.client.post(reverse('transactions:deposit_money'), {'amount': 100, 'transaction_type': DEPOSIT})
        self.assertRedirects(response, f"{reverse('accounts:user_login')}?next={reverse('transactions:deposit_money')}")
        
    def test_deposit_negative_amount(self):
        response = self.client.post(reverse('transactions:deposit_money'), {
            'amount': -100, 'transaction_type': DEPOSIT,
        })
        self.assertEqual(response.status_code, 200)  # Assume 200 if form re-renders with error
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))
        self.assertContains(response, "Amount must be positive")

class WithdrawFormTest(TestCase):  # Defines tests for WithdrawForm
    def setUp(self):  # Sets up a test account and minimum withdrawal amount
        user = User.objects.create_user(email='testuser@example.com', password='testpass')  # Creates a test user
        account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )  # Creates a "Saving" account type with specific limits
        self.account = UserBankAccount.objects.create(
            user=user, 
            account_type=account_type, 
            balance=1000.00,
            account_no='1234567890'
        )  # Creates a bank account for the user
        self.min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT = 10  # Sets minimum withdrawal amount to 10

    def test_withdraw_form_valid_data(self):  # Tests withdraw form with valid data
        form = WithdrawForm(data={'amount': 50}, account=self.account, initial={'transaction_type': WITHDRAWAL})
        if not form.is_valid():
            print(form.errors)  # Prints form errors if invalid
        self.assertTrue(form.is_valid())  # Asserts form is valid with the given data

    def test_withdraw_form_invalid_data(self):  # Tests withdraw form with invalid data
        form = WithdrawForm(data={'amount': 5}, account=self.account, initial={'transaction_type': WITHDRAWAL})
        self.assertFalse(form.is_valid())  # Checks form is invalid
        self.assertEqual(form.errors['amount'], [f'You can withdraw at least {self.min_withdraw_amount} $'])  # Checks error message

    def test_withdraw_exceeding_balance(self):
        response = self.client.post(reverse('transactions:withdraw_money'), {
            'amount': 1200, 'transaction_type': WITHDRAWAL,
        })
        self.assertEqual(response.status_code, 200)  # Assuming form re-renders with error
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))
        self.assertContains(response, "Insufficient funds")

    def test_withdraw_exceeding_max_limit(self):
        response = self.client.post(reverse('transactions:withdraw_money'), {
            'amount': 6000, 'transaction_type': WITHDRAWAL,
        })
        self.assertEqual(response.status_code, 200)  # Assuming error is displayed on the same page
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))
        self.assertContains(response, "Exceeds maximum withdrawal limit")


class TransactionViewsTest(TestCase):  # Defines tests for transaction-related views
    def setUp(self):  # Sets up test data and logs in the test user
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')  # Creates a test user
        self.account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000,
            annual_interest_rate=5.0,
            interest_calculation_per_year=12
        )  # Creates a "Saving" account type with specific limits
        self.account = UserBankAccount.objects.create(
            user=self.user, 
            account_type=self.account_type, 
            balance=1000.00,
            account_no='1234567890'
        )  # Creates a bank account for the user
        self.client.login(email='testuser@example.com', password='testpass')  # Logs in as the test user

    def test_deposit_money_view(self):  # Tests the deposit money view
        response = self.client.post(reverse('transactions:deposit_money'), {
            'amount': 200, 'transaction_type': DEPOSIT,
        })  # Sends a deposit request
        self.assertEqual(response.status_code, 302)  # Checks if it redirects after success
        self.account.refresh_from_db()  # Reloads account data from the database
        self.assertEqual(self.account.balance, Decimal('1200.00'))  # Checks the updated balance

    def test_withdraw_money_view(self):  # Tests the withdraw money view
        response = self.client.post(reverse('transactions:withdraw_money'), {
            'amount': 200, 'transaction_type': WITHDRAWAL,
        })  # Sends a withdrawal request
        self.assertEqual(response.status_code, 302)  # Checks if it redirects after success
        self.account.refresh_from_db()  # Reloads account data from the database
        self.assertEqual(self.account.balance, Decimal('800.00'))  # Checks the updated balance

    def test_transaction_report_view(self):  # Tests the transaction report view
        response = self.client.get(reverse('transactions:transaction_report'))  # Fetches the transaction report page
        self.assertEqual(response.status_code, 200)  # Checks if the page loads successfully
        self.assertTemplateUsed(response, 'transactions/transaction_report.html')  # Confirms correct template usage

class CalculateInterestTaskTest(TestCase):  # Defines tests for interest calculation task
    def setUp(self):  # Sets up account data for testing interest calculation
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')  # Creates a test user
        self.account_type = BankAccountType.objects.create(
            name='Saving', 
            maximum_withdrawal_amount=5000, 
            annual_interest_rate=5.0, 
            interest_calculation_per_year=12
        )  # Creates a "Saving" account type with specific limits
        current_month = timezone.now().month  # Gets the current month
        self.account = UserBankAccount.objects.create(
            user=self.user, 
            account_type=self.account_type, 
            balance=1000.00,
            initial_deposit_date=timezone.now() - relativedelta(months=12),  # Sets deposit date to 12 months ago
            interest_start_date=timezone.now() - relativedelta(months=current_month % 2 + 1),  # Sets start date
            # Verifies how interest calculations behave with slightly different starting points.
            account_no='1234567890'
        )  # Creates a bank account with interest calculation

        # date = datetime(2024, 11, 8)
        # new_date = date + relativedelta(months=3)  # Adds 3 months to the date
        # Result: datetime(2025, 2, 8)

    def test_calculate_interest(self):  # Tests the interest calculation function
        calculate_interest()  # Runs the interest calculation task
        self.account.refresh_from_db()  # Reloads account data from the database
        self.assertGreater(self.account.balance, Decimal('1000.00'))  # Checks if balance increased

    
