from django.contrib import admin
from .forms import UserForm
from .models import User

# Register your models here.
admin.site.register(User)
