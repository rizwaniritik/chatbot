from django.contrib import admin

from .models import Server, Category, Channel

# Register your models here.
admin.site.register(Server)
admin.site.register(Category)
admin.site.register(Channel)
