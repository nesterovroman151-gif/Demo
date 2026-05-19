import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Course, Application


class RegistrationForm(forms.Form):
    login = forms.CharField(
        max_length=150, label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин (латиница, 6+ символов)'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль (8+ символов)'}),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}),
        label='Подтверждение пароля'
    )
    full_name = forms.CharField(
        max_length=150, label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов Иван Иванович'})
    )
    phone = forms.CharField(
        max_length=20, label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (999) 123-45-67'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'})
    )

    def clean_login(self):
        login = self.cleaned_data['login']
        if len(login) < 6:
            raise ValidationError('Логин должен содержать минимум 6 символов')
        if not re.match(r'^[a-zA-Z0-9]+$', login):
            raise ValidationError(
                'Логин должен содержать только латинские буквы и цифры'
            )
        if User.objects.filter(username=login).exists():
            raise ValidationError('Такой логин уже занят')
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')
        return password

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise ValidationError('Пароли не совпадают')
        return cleaned


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=150, label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}),
        label='Пароль'
    )


class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'form-input',
            'pattern': '[0-9]{2}.[0-9]{2}.[0-9]{4}'
        }),
        label='Дата начала'
    )

    class Meta:
        model = Application
        fields = ['course', 'start_date', 'payment_method']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-input'}),
            'payment_method': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].empty_label = 'Выберите курс'
        self.fields['course'].label = 'Курс'
        self.fields['payment_method'].label = 'Способ оплаты'


class ReviewForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4, 'class': 'form-input',
            'placeholder': 'Напишите ваш отзыв о курсе...'
        }),
        label='Ваш отзыв'
    )
