from django import forms
from django.contrib.auth import password_validation
from .models import UserDetail


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserDetail
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        placeholders = {
            "first_name": "Enter First Name",
            "last_name": "Enter Last Name",
            "email": "Enter Email",
            "password": "Enter Password",
            "confirm_password": "Enter Confirm Password Again",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = placeholders.get(field_name, "")
            field.widget.attrs["class"] = "form-control"

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
