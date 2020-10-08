from django import forms
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput,CheckboxSelectMultiple
from .models import User
import datetime
from django.core.exceptions import ValidationError


class UserAdminForm(forms.ModelForm):
  class Meta:
    model = User
    widgets = {
      'password': PasswordInput(),
      # 'role': CheckboxSelectMultiple()
    }
    fields = '__all__'
  def clean(self):
    cleaned_data = super(UserAdminForm, self).clean()
    # self.cleaned_data['password'] = make_password(self.cleaned_data['password'])
    # self.cleaned_data['role'] = "STUDENT"
    if cleaned_data.get('dob') > datetime.date.today():
      raise ValidationError("Enter a valid Date of Birth")  
    if len(cleaned_data.get('phone_number')) < 4 or len(cleaned_data.get('phone_number')) >= 14:
      raise ValidationError("Phone Number length must be grater than 4 and less than 11 digits")
    if not str(cleaned_data.get('phone_number')).isnumeric():
      raise ValidationError("Phone Number must be a numeric value") 