from django import forms
from .models import LineRow

class LineRowForm(forms.ModelForm):
    class Meta:
        model = LineRow
        fields = '__all__'
        labels = {
            'plant_name' : '',
            'line_name' : '',
            'deviceId' : '',
            'name' : '',
            'deviceName' : '',
            'number' : '',
            'status' : '',
            'ip_camera' : '',
            'picturePath' : '',
            'guid' : '',
            'type' : '',
            'model' : '',
            'url' : '',
        }
        widgets = {
            'plant_name' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'line_name' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'deviceId' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'name' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'deviceName' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'number' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'status' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'ip_camera' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'guid' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'type' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'model' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
            'url' : forms.TextInput(attrs={
                'class' : 'input-hidden',
                'style' : 'display: none;'
                }),
        }