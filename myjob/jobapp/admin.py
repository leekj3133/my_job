from django.contrib.admin.filters import ChoicesFieldListFilter
# Register your models here.
from django.contrib import admin
from .models import Jobapp

class JobAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    fieldsets = [
        (None, {'fields': ["company"]}),
        (None, {"fields": ["url"]}),
    ]
    list_display = ("title", "company", "url")
    search_fields = ["question_text"]

admin.site.register(Jobapp, JobAdmin)




