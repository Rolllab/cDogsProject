from django import forms
from datetime import datetime

from dogs.models import Dog
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner', )

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        now_year = datetime.now().year
        if now_year - cleaned_data.year > 35:
            raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return cleaned_data