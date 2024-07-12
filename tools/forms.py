from django import forms
from .models import UserDetail


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=5)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserDetail
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
        if UserDetail.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("confirm_password")

        # password validation
        if password != re_password:
            raise forms.ValidationError({"password": ["Passwords does not match"]})
