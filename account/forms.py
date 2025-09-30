from django.contrib.auth.hashers import make_password
from django import forms

from .models import Account


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(max_length=50)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.lower().endswith("@catobi.com"):
            raise forms.ValidationError("Only Catobi.com emails are allowed.")
        return email


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.lower().endswith("@catobi.com"):
            raise forms.ValidationError("Only Catobi.com emails are allowed.")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
