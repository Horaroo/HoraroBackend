from django import forms
from django.contrib.auth import authenticate


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control-3 mt-3",
            'id': "inputUsername",
            "placeholder": "Логин",
            'style': "position: absolute;"
                     "bottom: 55%;"
                     "left: 45%;"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control-3 mt-3",
            'id': "inputPassword",
            "placeholder": "Пароль",
            'style': "position: absolute;"
                     "bottom: 50%;"
                     "left: 45%;"

        })
    )