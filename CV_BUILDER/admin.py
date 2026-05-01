from django.contrib import admin
from .models import CV, Template, Experience, Education, Skill, Language, Project

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'html_path')

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'template')

admin.site.register([Experience, Education, Skill, Language, Project])
