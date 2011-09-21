from django import forms

class Photo(forms.Form):
  filename = forms.CharField()
  photo = forms.FileField()
  
class Portrait():
  name = forms.CharField