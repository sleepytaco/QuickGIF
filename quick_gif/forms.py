from .models import QuickGIFs
from django import forms


class QuickGIFsForm(forms.Form):
    gif_file = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Images ')
    gif_speed = forms.FloatField(required=False, max_value=100, min_value=0, widget=forms.NumberInput(attrs={'placeholder': '0.5s', 'step': "0.1"}), label='GIF Speed')
    gif_width = forms.FloatField(required=False, max_value=1000, min_value=100, widget=forms.NumberInput(attrs={'placeholder': '500px'}), label='GIF Width')
    gif_height = forms.FloatField(required=False, max_value=1000, min_value=100, widget=forms.NumberInput(attrs={'placeholder': '550px', 'step': "1"}), label='GIF Height')
    set_height_from_width = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': "disableTxt()"}))
