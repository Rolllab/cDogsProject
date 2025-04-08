from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from users.models import User
from users.validators import validate_password


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        # fields = ('email', 'first_name', 'last_name', 'phone')    # Один из вариантов записи
        exclude = ('is_active', )                                   # Другой вариант записи


class UserRegisterForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        validate_password(cd['password'])
        if cd['password'] != cd['password2']:
            print('Пароли не совпадают!!!')
            raise forms.ValidationError('Пароли не совпадают !!!')
        return cd['password2']


class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    ...