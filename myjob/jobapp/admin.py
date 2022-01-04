from django.contrib import admin
from django.contrib import admin
from .models import GetInfo

class JobAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    fieldsets = [
        (None, {'fields': ["company"]}),
        (None, {"fields": ["url"]}),
        (None, {"fields": ["word"]}),
    ]
    list_display = ("title", "company", "url","word")
    search_fields = ["question_text"]

admin.site.register(GetInfo, JobAdmin)




