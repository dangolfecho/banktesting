from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
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

    def test_duplicate_email(self):
        User.objects.create(
            first_name="Existing",
            last_name="User",
            email="john@example.com",
            password="SecurePassword123",
            #account_type=self.bank_account_type,
            #gender="M",
            #birth_date="1990-01-01"
        )
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',  # Duplicate email
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('email', form.errors)

    def test_birth_date_in_future(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '2090-01-01'  # Date in the future
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('birth_date', form.errors)

    def test_password_minimum_length(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': '123',  # Password too short
            'password2': '123',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('password1', form.errors)

    def test_password_complexity(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'password',  # Simple password lacking complexity
            'password2': 'password',
            'account_type': self.bank_account_type.pk,
            'gender': 'M',
            'birth_date': '1990-01-01'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('password1', form.errors)
    
class AddressFormTests(TestCase):
    def test_valid_address_form(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_street_address_required(self):
        form_data = {
            'street_address': '',
            'city': 'Anytown',
            'postal_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('street_address', form.errors)

    def test_city_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': '',
            'postal_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('city', form.errors)

    def test_postal_code_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('postal_code', form.errors)

    def test_country_required(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '90210',
            'country': ''
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('country', form.errors)

    def test_postal_code_format(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': 'invalid_zip',  # Invalid format
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('postal_code', form.errors)

    def test_invalid_country(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '90210',
            'country': 'InvalidCountry'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('country', form.errors)

    def test_city_minimum_length(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'A',  # City too short
            'postal_code': '90210',
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('city', form.errors)

    def test_postal_code_numeric_only(self):
        form_data = {
            'street_address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '90a210',  # Alphanumeric postal code
            'country': 'USA'
        }
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('postal_code', form.errors)

class LoginViewTests(TestCase):
    def setUp(self):
        # Set up a test user
        self.username = "211111@iiitt.ac.in"
        self.password = "glassitem"
        #self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_page_loads(self):
        # Check that the login page loads correctly
        response = self.client.get(reverse('accounts:user_login'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_login.html')  
        #self.assertContains(response, "Sign In")

    def test_successful_login(self):
        # Attempt to log in with correct credentials
        response = self.client.post(reverse('accounts:user_login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('home'))  
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_username(self):
        # Attempt to log in with an incorrect username
        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'wronguser',
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "Error!")

    def test_invalid_password(self):
        # Attempt to log in with an incorrect password
        response = self.client.post(reverse('accounts:user_login'), {
            'username': self.username,
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "Error!")  # Check if error message block is displayed

    def test_missing_username(self):
        # Attempt to log in without a username
        response = self.client.post(reverse('accounts:user_login'), {
            'username': '',
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "This field is required.")  # Django form validation error

    def test_missing_password(self):
        # Attempt to log in without a password
        response = self.client.post(reverse('accounts:user_login'), {
            'username': self.username,
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, "This field is required.")  # Django form validation error

    def test_csrf_token_present(self):
        # Check if the CSRF token is present in the login form
        response = self.client.get(reverse('accounts:user_login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_redirection_for_authenticated_user(self):
        # Log in the user first
        self.client.login(username=self.username, password=self.password)
        
        # Try to access the login page again while logged in
        response = self.client.get(reverse('accounts:user_login'))
        self.assertRedirects(response, reverse('home'))  # Adjust as needed for post-login redirection

    def test_non_field_error_display(self):
        # Test non-field errors by providing invalid credentials
        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error!")  # Checks if the template's error div is rendered