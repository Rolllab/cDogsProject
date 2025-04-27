from django import forms
from datetime import datetime

from dogs.models import Dog, DogParent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data:
            now_year = datetime.now().year
            if now_year - cleaned_data.year > 35:
                raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return cleaned_data


class DogAdminForm(DogForm):
    class Meta:
        model = Dog
        exclude = ('is_active',)

    # def clean_birth_date(self):
    #     cleaned_birth_date = super().clean_birth_date()
    #     return cleaned_birth_date


class DogParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = DogParent
        fields = '__all__'
