from django.contrib import admin
from .models import ContactForm

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'interests', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email']
    readonly_fields = ['id', 'created_at']