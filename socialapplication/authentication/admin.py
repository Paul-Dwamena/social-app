from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'following_count', 'follower_count')
