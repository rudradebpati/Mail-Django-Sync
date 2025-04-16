from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserDetails)
# class UserDetail(admin.ModelAdmin):
class UserDetails(admin.ModelAdmin):
    list_display = [field.name for field in UserDetails._meta.fields]
    # search_fields = ('__all__',)
    search_fields = (
        "email",
        "username",
        "id",
    )