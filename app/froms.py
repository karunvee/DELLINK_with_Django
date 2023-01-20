from django import forms
from .models import LineRow

class MyModelForm(forms.ModelForm):
    class Meta:
        model = LineRow
        fields = ('image',)
