from django import forms
from .models import LineRow

class LineRowForm(forms.ModelForm):
    class Meta:
        model = LineRow
        fields = '__all__'