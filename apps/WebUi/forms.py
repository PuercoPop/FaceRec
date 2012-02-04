
from django.forms import ModelForm
from django import forms


class PhotoForm(forms.Form):
  title = forms.CharField(max_length=50)
  photo = forms.FileField()
  
class PortraitForm(forms.Form):
  name = forms.CharField
