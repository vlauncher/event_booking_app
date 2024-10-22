# users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm as DefaultSignupForm, ChangePasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SignUpForm(DefaultSignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'spam.com' in email:
            raise ValidationError("Registration from 'spam.com' domain is prohibited.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain alphabetic characters.")
        return first_name

    def save(self, request):
        user = super(SignUpForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        """Override to implement custom validation on user login."""
        if not user.is_active:
            raise forms.ValidationError(_('This account is inactive.'), code='inactive')

    def clean(self):
        """Custom clean method to perform additional validations."""
        cleaned_data = super().clean()
        email = cleaned_data.get('username')  # The 'username' field is the email in your case
        password = cleaned_data.get('password')

        # Add any custom validation here (e.g., check if email is in a specific domain)
        if email and password:
            if not email.endswith('@example.com'):
                raise forms.ValidationError(_('Login is restricted to @example.com emails.'), code='invalid_email')

        return cleaned_data


class CustomPasswordChangeForm(ChangePasswordForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        required=True,
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        required=True,
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', _("The two password fields didn't match."))

        if new_password1 and len(new_password1) < 8:
            self.add_error('new_password1', _("Password must be at least 8 characters long."))

        return cleaned_data


# users/views.py

# users/forms.py

from django import forms
from .models import Profile

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address']  # Include fields to be updated
        widgets = { 
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Add any custom validation for phone number here
        return phone_number
