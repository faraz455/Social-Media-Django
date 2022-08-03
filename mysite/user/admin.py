from django.contrib import admin
from .models import CustomUser,Posts, Follower
# Register your models here.

admin.site.register((CustomUser,Posts,Follower))