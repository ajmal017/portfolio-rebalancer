# from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth.models import Group
from .forms import UserAdminForm
from django.db.models import Q
# Register your models here.

admin.site.unregister(Group)
# admin.site.unregister(Token)

