from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=5)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        placeholders = {
            "first_name": "Bijoy",
            "last_name": "Joseph",
            "email": "example@gmail.com",
            "password": "*********",
            "confirm_password": "*********",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = placeholders.get(field_name, "")
            field.widget.attrs["class"] = "w-full p-2 border border-gray-300 rounded mt-1"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email.lower()).exists():
            raise forms.ValidationError("This Email already exists.")
        return email.lower()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        placeholders = {
            "email": "example@gmail.com",
            "password": "*********",
        }

        for field_name, field in self.fields.items():
            field.widget.attrs["placeholder"] = placeholders.get(field_name, "")
            field.widget.attrs["class"] = "w-full p-2 border border-gray-300 rounded mt-1"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email.lower()).exists():
            raise forms.ValidationError("This Email does not exist.")
        return email.lower()
