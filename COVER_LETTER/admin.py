from django.contrib import admin
from .models import CoverLetter, CoverLetterTemplate

@admin.register(CoverLetterTemplate)
class CoverLetterTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'html_path')

@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'recipient_name', 'company_name', 'created_at')
    list_filter = ('user', 'template')
