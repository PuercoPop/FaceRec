from django import forms

class PhotoForm(forms.Form):
  filename = forms.CharField(max_length=50)
  photo = forms.FileField()
  
class Portrait():
  name = forms.CharField