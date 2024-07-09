from django import forms
from .models import UserDetails
from django.contrib.auth import password_validation


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("confirm_password")

        # password validation
        if password != re_password:
            raise forms.ValidationError({"password": ["Passwords does not match"]})

        if password is None:
            raise forms.ValidationError({"password": ["Password can't be empty"]})
        try:
            password_validation.validate_password(password=password)
        except forms.ValidationError as error:
            raise forms.ValidationError({"password": error})