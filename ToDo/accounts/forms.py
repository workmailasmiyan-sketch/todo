from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

        labels = {
            'username': 'Логин',
            'email': 'Email',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует")

        return username

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1:
            if len(password1) < 8:
                raise ValidationError("Пароль должен содержать минимум 8 символов")

            if password1.isdigit():
                raise ValidationError("Пароль не может состоять только из цифр")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class SimplePasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')

        if p1:
            if len(p1) < 8:
                raise ValidationError("Пароль должен содержать минимум 8 символов")

            if p1.isdigit():
                raise ValidationError("Пароль не может состоять только из цифр")

        if p1 and p2:
            if p1 != p2:
                raise ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user