from django import forms
from django.forms import PasswordInput, CheckboxSelectMultiple
from .models import Teacher
import datetime
from django.core.exceptions import ValidationError
from modules.configurations.models import MusicGenre

class TeacherAdminForm(forms.ModelForm):
  class Meta:
    model = Teacher
    # widgets = {
    #   'password': PasswordInput(),
    #    'music_genres': CheckboxSelectMultiple(),
    #    'instruments': CheckboxSelectMultiple()
    #    }
    fields = '__all__'
  def clean(self):
    # https://stackoverflow.com/questions/15456964/changing-password-in-django-admin/15630360
    cleaned_data = super(TeacherAdminForm, self).clean()
    # if cleaned_data.get('dob') > datetime.date.today():
    #   raise ValidationError("Enter a valid Date of Birth")  
    # if len(cleaned_data.get('phone_number')) < 4 or len(cleaned_data.get('phone_number')) >= 10:
    #   raise ValidationError("Phone Number length must be greater than 4 and less than 11 digits")  
    # if not str(cleaned_data.get('phone_number')).isnumeric():
    #   raise ValidationError("Phone Number must be a numeric value")  
    if cleaned_data.get('experience') < 0:
      raise ValidationError("Experience cannot be a negative value")  

  