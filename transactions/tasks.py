from django.utils import timezone

from celery import shared_task
from accounts.models import UserBankAccount
from transactions.constants import INTEREST
from transactions.models import Transaction


@shared_task
def calculate_interest():
    accounts = UserBankAccount.objects.filter(
        balance__gt=0,
        interest_start_date__lte=timezone.now(),
        initial_deposit_date__isnull=False
    ).select_related('account_type')

    this_month = timezone.now().month
    print(f"Current month: {this_month}")  # Debug statement

    created_transactions = []
    updated_accounts = []

    for account in accounts:
        print(f"Processing account: {account.account_no}")  # Debug statement
        print(f"Account balance: {account.balance}")  # Debug statement
        print(f"Interest calculation months: {account.get_interest_calculation_months()}")  # Debug statement

        if this_month in account.get_interest_calculation_months():
            interest = account.account_type.calculate_interest(account.balance)
            print(f"Calculated interest: {interest}")  # Debug statement

            account.balance += interest
            account.save()

            transaction_obj = Transaction(
                account=account,
                transaction_type=INTEREST,
                amount=interest,
                balance_after_transaction=account.balance  # Ensure this field is set
            )
            created_transactions.append(transaction_obj)
            updated_accounts.append(account)

            print(f"Updated balance: {account.balance}")  # Debug statement

    if created_transactions:
        Transaction.objects.bulk_create(created_transactions)

    if updated_accounts:
        UserBankAccount.objects.bulk_update(updated_accounts, ['balance'])
