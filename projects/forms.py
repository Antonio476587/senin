from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EditOwnerNickname(forms.Form):
    nickname = forms.CharField(max_length=50, required=True, help_text='You must to provide a nickname broda.')

    def clean_nickname(self):
        data = self.cleaned_data['nickname']

        if not data.isprintable():
            raise ValidationError('Your nickname is not printable')

        if data.isdigit():
            raise ValidationError('Add some characters, it is not R2D2')

        return data
