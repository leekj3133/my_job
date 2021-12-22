from django.contrib import admin
from .models import Job

from django.contrib.admin.filters import ChoicesFieldListFilter
# Register your models here.

class JobAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    fieldsets = [
        (None, {'fields': ["company"]}),
        (None, {"fields": ["url"]}),
    ]
    list_display = ("title", "company", "url")
    search_fields = ["question_text"]

admin.site.register(Job, JobAdmin)

# from .models import Choice, Question



