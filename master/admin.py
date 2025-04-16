from django.contrib import admin
from .models import EmailStorage
# Register your models here.
@admin.register(EmailStorage)
class EmailStorage(admin.ModelAdmin):
    list_display = [field.name for field in EmailStorage._meta.fields]
    search_fields = (
        "subject",
        "sender",
        "body_preview",
        "date_received",
    )
