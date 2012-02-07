
from django.forms import ModelForm, FileInput
from django import forms
from models import Photo


class UploadForm(ModelForm):
  class Meta:
    model = Photo
    widgets = { 
      'path': FileInput(attrs={
          'class':'left_column',
          'name':'file',
          'value':'Choose Photo',
          }),
      }


