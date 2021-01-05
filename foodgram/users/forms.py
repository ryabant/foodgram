from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')
        labels = {
            'first_name': 'Имя',
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
