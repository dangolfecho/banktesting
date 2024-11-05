from django.test import TestCase
from .forms import UserRegistrationForm, UserAddressForm   
from .models import User, BankAccountType


class UserRegistrationFormTests(TestCase):
    def setUp(self):
        self.bank_account_type = BankAccountType.objects.create(
            name="Basic",
            maximum_withdrawal_amount=1000,
            annual_interest_rate=5,
            interest_calculation_per_year=12
        )

    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        form_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('first_name', form.errors)

    def test_last_name_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': '',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('last_name', form.errors)

    def test_email_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('email', form.errors)

    def test_email_invalid_format(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('email', form.errors)

    def test_password1_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': '',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('password1', form.errors)

    def test_password2_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': '',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('password2', form.errors)

    def test_passwords_match(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'DifferentPassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('password2', form.errors)

    def test_account_type_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('account_type', form.errors)

    def test_gender_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': '',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('gender', form.errors)

    def test_birth_date_required(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('birth_date', form.errors)

    def test_birth_date_format(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '01-01-1990'  # Invalid format
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('birth_date', form.errors)


    
class UserRegistrationFormTests(TestCase):
    def setUp(self):
        self.bank_account_type = BankAccountType.objects.create(
            name="Basic",
            maximum_withdrawal_amount=1000,
            annual_interest_rate=5,
            interest_calculation_per_year=12
        )

    def test_valid_user_registration_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    # ... [Include all previous tests for UserRegistrationForm here] ...

class AddressFormTests(TestCase):
    def test_valid_address_form(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_street_address_required(self):
        form_data = {
            'street_address': '',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('street_address', form.errors)

    def test_city_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': '',
            'state': 'CA',
            'zip_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('city', form.errors)

    def test_state_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'state': '',
            'zip_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        print('dfsfds')

        self.assertIn(UserAddressForm(data=form_data), form.errors)
        print('dfsfds')

    def test_zip_code_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('zip_code', form.errors)

    def test_country_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '90210',
            'country': ''
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('country', form.errors)

    def test_zip_code_format(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': 'invalid_zip',  # Invalid format
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('zip_code', form.errors)

    # Additional test cases for address validation can be added here.
